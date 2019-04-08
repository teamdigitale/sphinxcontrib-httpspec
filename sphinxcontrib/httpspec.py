"""Sphinx extension that embeds Mozilla topics in documents."""

from __future__ import print_function

import sys

import sphinx
from docutils import nodes
from docutils.parsers.rst import roles
from sphinx import addnodes
from sphinx.errors import ExtensionError, SphinxError

if sphinx.version_info < (2,):
    from .compat import ReferenceRole
else:
    from sphinx.util.docutils import ReferenceRole

if sys.version_info < (3,):
    import httplib as httpclient
else:
    import http.client as httpclient

__author__ = "Team per la Trasformazione Digitale"
__license__ = "BSD-3-clause"
__version__ = "0.0.1"


class MozillaError(SphinxError):
    """Non-configuration error. Raised when Role has bad options."""

    category = "Mozilla option error"


def _is_status(role):
    """Returns true if the line describes an existing http status."""

    if role.name != "httpstatus":
        return False
    if not role.target:
        return False
    if role.target.isdigit() and int(role.target) in httpclient.responses:
        return True
    return False


class HTTPRole(ReferenceRole):
    NAME_MAP = {"status": "Status", "header": "Headers", "method": "Methods"}

    def run(self):
        # type: () -> Tuple[List[nodes.Node], List[nodes.system_message]]  # NOQA
        target_id = "index-%s" % self.env.new_serialno("index")

        self.http_type = self.name.lower()[4:]
        if self.http_type not in HTTPRole.NAME_MAP:
            msg = self.inliner.reporter.error(
                "invalid HTTP reference %s" % self.name, line=self.lineno
            )
            prb = self.inliner.problematic(self.rawtext, self.rawtext, msg)
            return [prb], [msg]

        entries = [
            (
                "single",
                "HTTP; HTTP %s %s" % (self.http_type, self.target),
                target_id,
                "",
                None,
            )
        ]

        index = addnodes.index(entries=entries)
        target = nodes.target("", "", ids=[target_id])
        self.inliner.document.note_explicit_target(target)

        try:
            refuri = self.build_uri()
            reference = nodes.reference(
                "", "", internal=False, refuri=refuri, classes=["rfc"]
            )
            if self.has_explicit_title:
                reference += nodes.strong(self.title, self.title)
            else:
                title = "HTTP %s %s " % (self.http_type, self.target)
                if _is_status(self):
                    title += " " + httpclient.responses[int(self.target)]
                reference += nodes.strong(title, title)
        except ValueError:
            msg = self.inliner.reporter.error(
                "invalid HTTP mozilla reference %s" % self.target, line=self.lineno
            )
            prb = self.inliner.problematic(self.rawtext, self.rawtext, msg)
            return [prb], [msg]

        return [index, target, reference], []

    def build_uri(self):
        # type: () -> str
        base_url = "https://developer.mozilla.org/en-US/docs/Web/HTTP"
        return "/".join((base_url, HTTPRole.NAME_MAP[self.http_type], self.target))


def setup(app):
    """Called by Sphinx during phase 0 (initialization).

    :param app: Sphinx application object.

    :returns: Extension version.
    :rtype: dict
    """
    roles.register_local_role("httpstatus", HTTPRole())
    roles.register_local_role("httpmethod", HTTPRole())
    roles.register_local_role("httpheader", HTTPRole())

    return {"version": __version__}
