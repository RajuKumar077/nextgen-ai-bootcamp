import sys, nbformat
from nbclient import NotebookClient
src, dst = sys.argv[1], sys.argv[2]
nb = nbformat.read(src, 4)
NotebookClient(nb, timeout=600, kernel_name="python3", resources={"metadata": {"path": src.rsplit("/", 1)[0]}}, allow_errors=True).execute()
nbformat.write(nb, dst)
errs = [(c.source.splitlines()[0][:60], o.get("ename"), o.get("evalue", "")[:140]) for c in nb.cells if c.cell_type == "code" for o in c.outputs if o.get("output_type") == "error"]
print(dst.rsplit("/", 1)[1], "| errors:", errs or "NONE")
