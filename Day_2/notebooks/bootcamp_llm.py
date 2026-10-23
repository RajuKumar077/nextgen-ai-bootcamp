"""
bootcamp_llm.py · Helper for the "GenAI & Agentic AI for SAP Professionals" bootcamp.

Talks to a LOCAL Ollama server. Uses only the Python standard library, so there is nothing to pip-install.
The model name is a PLACEHOLDER: set it in ../bootcamp_config.json or with the BOOTCAMP_MODEL environment variable.

Participants never need to read this file. Notebooks just do:  from bootcamp_llm import *
"""
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request

if sys.platform == "win32":
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8")
        if hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


# ───────────────────────────── configuration ─────────────────────────────
_HERE = os.path.dirname(os.path.abspath(__file__))
_DEFAULTS = {
    "ollama_url": "http://localhost:11434",
    "model": "llama3.2:3b",          # ← PLACEHOLDER: main model
    "small_model": "llama3.2:1b",    # ← PLACEHOLDER: small/fast model (security & temperature demos)
    "num_ctx": 8192,                 # context window to request from Ollama
    "timeout_seconds": 300,
}


def _load_config():
    cfg = dict(_DEFAULTS)
    for folder in (_HERE, os.path.dirname(_HERE)):
        path = os.path.join(folder, "bootcamp_config.json")
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                cfg.update({k: v for k, v in json.load(f).items() if not k.startswith("_")})
            cfg["_config_file"] = path
            break
    # environment variables win (handy for quick switches)
    if os.getenv("OLLAMA_HOST"):
        host = os.getenv("OLLAMA_HOST")
        cfg["ollama_url"] = host if host.startswith("http") else "http://" + host
    cfg["model"] = os.getenv("BOOTCAMP_MODEL", cfg["model"])
    cfg["small_model"] = os.getenv("BOOTCAMP_SMALL_MODEL", cfg["small_model"])
    return cfg


CONFIG = _load_config()
MODEL = CONFIG["model"]
SMALL_MODEL = CONFIG["small_model"]
OLLAMA_URL = CONFIG["ollama_url"].rstrip("/")

last_usage = {}          # filled after every call: input_tokens, output_tokens, seconds, model
_caps_cache = {}


class BootcampError(RuntimeError):
    """A friendly error with a clear 'how to fix' message."""


# ───────────────────────────── low-level HTTP ─────────────────────────────
def _post(path, body, stream=False):
    req = urllib.request.Request(
        OLLAMA_URL + path,
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    try:
        resp = urllib.request.urlopen(req, timeout=CONFIG["timeout_seconds"])
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "ignore")
        if e.code == 404 and "not found" in detail.lower():
            raise BootcampError(
                f"Model '{body.get('model')}' is not downloaded.\n"
                f"👉 Fix: open a terminal and run:   ollama pull {body.get('model')}"
            ) from None
        raise BootcampError(f"Ollama returned HTTP {e.code}: {detail[:300]}") from None
    except urllib.error.URLError:
        raise BootcampError(
            f"Cannot reach Ollama at {OLLAMA_URL}.\n"
            "👉 Fix: start the Ollama app (Windows: Start menu → Ollama), or run:   ollama serve"
        ) from None
    if stream:
        return resp
    return json.loads(resp.read().decode("utf-8"))


def _get(path):
    try:
        with urllib.request.urlopen(OLLAMA_URL + path, timeout=10) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.URLError:
        raise BootcampError(
            f"Cannot reach Ollama at {OLLAMA_URL}.\n"
            "👉 Fix: start the Ollama app (Windows: Start menu → Ollama), or run:   ollama serve"
        ) from None


def _capabilities(model):
    if model not in _caps_cache:
        try:
            _caps_cache[model] = _post("/api/show", {"model": model}).get("capabilities") or []
        except BootcampError:
            _caps_cache[model] = []
    return _caps_cache[model]


def _base_body(model, messages, temperature, max_tokens):
    body = {"model": model, "messages": messages, "stream": False,
            "options": {"num_ctx": CONFIG["num_ctx"]}}
    if temperature is not None:
        body["options"]["temperature"] = temperature
    if max_tokens is not None:
        body["options"]["num_predict"] = max_tokens
    if "thinking" in _capabilities(model):
        body["think"] = False          # keep answers fast and clean for teaching
    return body


def _set_usage(r, t0, model):
    # mutate in place, so `from bootcamp_llm import last_usage` always sees fresh numbers
    last_usage.clear()
    last_usage.update({"input_tokens": r.get("prompt_eval_count", 0), "output_tokens": r.get("eval_count", 0),
                       "seconds": round(time.time() - t0, 1), "model": model})


# ───────────────────────────── public helpers ─────────────────────────────
def chat(messages, system=None, temperature=None, max_tokens=None, model=None):
    """Send a whole conversation (list of {'role','content'}) and return the reply text."""
    model = model or MODEL
    msgs = ([{"role": "system", "content": system}] if system else []) + list(messages)
    t0 = time.time()
    r = _post("/api/chat", _base_body(model, msgs, temperature, max_tokens))
    _set_usage(r, t0, model)
    return (r.get("message", {}).get("content") or "").strip()


def ask_ai(question, system=None, temperature=None, max_tokens=None, model=None):
    """One question in, one answer out:  INPUT → AI → OUTPUT."""
    return chat([{"role": "user", "content": question}], system=system,
                temperature=temperature, max_tokens=max_tokens, model=model)


def ask_small(question, system=None, temperature=None, max_tokens=None):
    """Same as ask_ai, but uses the SMALL model (security and temperature demos)."""
    return ask_ai(question, system=system, temperature=temperature, max_tokens=max_tokens, model=SMALL_MODEL)


def stream_ai(question, system=None, model=None):
    """Print the answer piece by piece, as the model writes it."""
    model = model or MODEL
    msgs = ([{"role": "system", "content": system}] if system else []) + [{"role": "user", "content": question}]
    body = _base_body(model, msgs, None, None)
    body["stream"] = True
    with _post("/api/chat", body, stream=True) as resp:
        for line in resp:
            if line.strip():
                piece = json.loads(line).get("message", {}).get("content", "")
                print(piece, end="", flush=True)
    print()


def parse_json(text):
    """Turn an AI reply into a Python dict. Removes ```json fences and any text around the JSON."""
    cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip())
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", cleaned, re.S)
        if match:
            return json.loads(match.group(0))
        raise


def ask_json(question, system=None, schema=None, temperature=0, max_tokens=400, model=None):
    """Ask for JSON and return a dict.
    Uses Ollama's structured-output mode when the model supports it, and falls back to prompt + parse when it doesn't."""
    model = model or MODEL
    msgs = ([{"role": "system", "content": system}] if system else []) + [{"role": "user", "content": question}]
    body = _base_body(model, msgs, temperature, max_tokens)
    body["format"] = schema or "json"
    t0 = time.time()
    try:
        r = _post("/api/chat", body)
        text = r.get("message", {}).get("content", "")
        _set_usage(r, t0, model)
        last_usage["mode"] = "structured"
    except BootcampError as e:
        if "structured output" not in str(e).lower() and "format" not in str(e).lower():
            raise
        text = chat(msgs, temperature=temperature, max_tokens=max_tokens, model=model)
        last_usage["mode"] = "prompt+parse"
    return parse_json(text)


def show(text):
    """Display an AI answer nicely (tables, bold, bullets) inside Jupyter."""
    try:
        from IPython.display import Markdown, display
        display(Markdown(text))
    except ImportError:
        print(text)


def check_setup(verbose=True):
    """Check that Ollama is running and both models are downloaded. Prints clear fixes if not."""
    ok = True
    try:
        version = _get("/api/version").get("version", "?")
        installed = {m["name"] for m in _get("/api/tags").get("models", [])}
    except BootcampError as e:
        print("❌", e)
        return False
    names = installed | {n.split(":")[0] for n in installed if n.endswith(":latest")}
    if verbose:
        print(f"✅ Ollama {version} is running at {OLLAMA_URL}")
    for label, m in (("Main model ", MODEL), ("Small model", SMALL_MODEL)):
        if m in names or f"{m}:latest" in installed:
            if verbose:
                print(f"✅ {label}: {m}")
        else:
            ok = False
            print(f"❌ {label}: {m} is not downloaded  →  run:   ollama pull {m}")
    if verbose and CONFIG.get("_config_file"):
        print(f"⚙️  Config: {CONFIG['_config_file']}")
    return ok


__all__ = ["CONFIG", "MODEL", "SMALL_MODEL", "OLLAMA_URL", "last_usage", "BootcampError",
           "chat", "ask_ai", "ask_small", "stream_ai", "ask_json", "parse_json", "show", "check_setup"]
