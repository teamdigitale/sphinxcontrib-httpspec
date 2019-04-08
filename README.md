# Sphinx extension that provide inlines references to HTTP specs

## Installation

```console
pip install git+https://github.com/teamdigitale/sphinxcontrib-httpspec
```

Add `sphinxcontrib.httpspec` to `extensions` in your `conf.py`.

## Usage

Whenever you want to reference an http component defined in the specs,
use the roles in the rST source of your documentation like
this:

```rst

On success, you should return :httpstatus:`200` and 
use the :httpheader:`Location` to reference the returned resource.

```

This will point to:

  - https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Location

Supported roles:

  - :httpheader:
  - :httpstatus:
  - :httpmethod:

## Licenses

`BSD-3-Clause`.
