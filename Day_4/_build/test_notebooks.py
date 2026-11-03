"""Runs a Day 4 notebook top to bottom, in-process, against the mock model (see mock_model.py). No Jupyter kernel and no Ollama needed.

    python test_notebooks.py <notebook.ipynb> [--approve yes|no] [--keep-going]

It prints every cell's output and stops at the first error (unless --keep-going). A clean run proves the plumbing works:
the MCP server starts, tools are discovered and called, gates and limits fire, and the checks pass.
"""
import contextlib
import io
import json
import os
import sys
import traceback

BUILD = os.path.dirname(os.path.abspath(__file__))
DAY4 = os.path.dirname(BUILD)
sys.path.insert(0, BUILD)
sys.path.insert(0, DAY4 + "/shared")
import bootcamp_llm      # noqa: E402
import mock_model        # noqa: E402

bootcamp_llm._post = mock_model.post
bootcamp_llm._get = mock_model.get


def run(path, approve="yes", keep_going=False, quiet=False):
    nb = json.load(open(path, encoding="utf-8"))
    os.chdir(os.path.dirname(os.path.abspath(path)))
    os.environ["BOOTCAMP_AUTO_APPROVE"] = approve
    import builtins
    builtins.input = lambda prompt="": (print(prompt + approve), approve)[1]
    ns, errors, outputs = {"__name__": "__main__"}, [], []
    for cell in nb["cells"]:
        if cell["cell_type"] != "code":
            continue
        src = "".join(cell["source"])
        tag = src.splitlines()[0][:70]
        buf = io.StringIO()
        try:
            with contextlib.redirect_stdout(buf):
                exec(compile(src, tag, "exec"), ns)
        except Exception:
            errors.append((tag, traceback.format_exc(limit=3)))
        outputs.append((tag, buf.getvalue()))
        if not quiet:
            print("=" * 100 + "\n" + tag + "\n" + "-" * 100 + "\n" + buf.getvalue().rstrip())
        if errors and not keep_going:
            break
    for name in ("client", "mcp"):
        with contextlib.suppress(Exception):
            ns[name].close()
    return ns, errors, outputs


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    approve = sys.argv[sys.argv.index("--approve") + 1] if "--approve" in sys.argv else "yes"
    if approve in args:
        args.remove(approve)
    ns, errors, _ = run(args[0], approve, "--keep-going" in sys.argv)
    print("\n" + ("ERRORS:\n" + "\n".join(f"  {t}\n{tb}" for t, tb in errors) if errors else f"✅ {os.path.basename(args[0])}: no errors"))
    sys.exit(1 if errors else 0)
