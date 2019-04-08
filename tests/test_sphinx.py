from subprocess import run
from shlex import split
from pathlib import Path


def test_sphinx():
    cmd =  "sphinx-build -b html tests tests/_build/"
    Path('tests/index.rst').write_text("""ciao\n====\n Ciao :httpstatus:`200`\nCiao :httpmethod:`POST`\nCiao :httpheader:`Location`\n """)
    run(split(cmd))
   
    results = Path('tests/_build/index.html').read_text()
    for needle in [
    '<strong>HTTP status 200  OK</strong>',
    'https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST',
    'https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Location'
    ]: 
        assert needle in results, "Missing %r" % needle 


