from pathlib import Path
from shlex import split
from shutil import rmtree

try:
    from subprocess import run
except ImportError:
    from subprocess import check_output as run


def setup():
    ifile = Path("tests/index.rst")
    if ifile.exists():
        ifile.unlink()
    if Path("tests/_build").exists():
        rmtree("tests/_build")


def test_sphinx():
    cmd = "sphinx-build -b html tests tests/_build/"
    with open("tests/index.rst", "w") as fh:
        fh.write(
            """ciao\n====\nCiao :httpstatus:`200`\nCiao :httpmethod:`POST`\nCiao :httpheader:`Location`\n\n"""
        )
    run(split(cmd))

    with open("tests/_build/index.html") as fh:
        results = fh.read()
    for needle in [
        "<strong>HTTP status 200  OK</strong>",
        "https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST",
        "https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Location",
    ]:
        assert needle in results, "Missing %r" % needle
