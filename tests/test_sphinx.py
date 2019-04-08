from pathlib import Path
from shlex import split
from shutil import rmtree
from subprocess import run


def setup():
    ifile = Path("tests/index.rst")
    if ifile.exists():
        ifile.unlink()
    if Path("tests/_build").exists():
        rmtree("tests/_build")


def test_sphinx():
    cmd = "sphinx-build -b html tests tests/_build/"
    Path("tests/index.rst").write_text(
        """ciao\n====\nCiao :httpstatus:`200`\nCiao :httpmethod:`POST`\nCiao :httpheader:`Location`\n\n"""
    )
    run(split(cmd))

    results = Path("tests/_build/index.html").read_text()
    for needle in [
        "<strong>HTTP status 200  OK</strong>",
        "https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST",
        "https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Location",
    ]:
        assert needle in results, "Missing %r" % needle
