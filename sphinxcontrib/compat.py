"""
Compatibility classes for sphinx <1.7
"""
import re

from docutils.utils import unescape


class SphinxRole(object):
    """A base class for Sphinx roles.

    This class provides helper methods for Sphinx roles.

    .. note:: The subclasses of this class might not work with docutils.
              This class is strongly coupled with Sphinx.
    """

    name = None  #: The role name actually used in the document.
    rawtext = None  #: A string containing the entire interpreted text input.
    text = None  #: The interpreted text content.
    lineno = None  #: The line number where the interpreted text begins.
    inliner = None  #: The ``docutils.parsers.rst.states.Inliner`` object.
    options = None  #: A dictionary of directive options for customization
    #: (from the "role" directive).
    content = None  #: A list of strings, the directive content for customization

    #: (from the "role" directive).

    def __call__(self, name, rawtext, text, lineno, inliner, options={}, content=[]):
        # type: (str, str, str, int, Inliner, Dict, List[str]) -> Tuple[List[nodes.Node], List[nodes.system_message]]  # NOQA
        self.rawtext = rawtext
        self.text = unescape(text)
        self.lineno = lineno
        self.inliner = inliner
        self.options = options
        self.content = content

        # guess role type
        if name:
            self.name = name.lower()
        else:
            self.name = self.env.temp_data.get("default_role")
            if not self.name:
                self.name = self.env.config.default_role
            if not self.name:
                raise SphinxError("cannot determine default role!")

        return self.run()

    @property
    def env(self):
        # type: () -> BuildEnvironment
        """Reference to the :class:`.BuildEnvironment` object."""
        return self.inliner.document.settings.env

    @property
    def config(self):
        # type: () -> Config
        """Reference to the :class:`.Config` object."""
        return self.env.config

    def set_source_info(self, node, lineno=None):
        # type: (nodes.Node, int) -> None
        if lineno is None:
            lineno = self.lineno

        source_info = self.inliner.reporter.get_source_and_line(lineno)  # type: ignore
        node.source, node.line = source_info


class ReferenceRole(SphinxRole):
    """A base class for reference roles.

    The reference roles can accpet ``link title <target>`` style as a text for
    the role.  The parsed result; link title and target will be stored to
    ``self.title`` and ``self.target``.
    """

    has_explicit_title = (
        None
    )  #: A boolean indicates the role has explicit title or not.
    title = None  #: The link title for the interpreted text.
    target = None  #: The link target for the interpreted text.

    # \x00 means the "<" was backslash-escaped
    explicit_title_re = re.compile(r"^(.+?)\s*(?<!\x00)<(.*?)>$", re.DOTALL)

    def __call__(self, name, rawtext, text, lineno, inliner, options={}, content=[]):
        # type: (str, str, str, int, Inliner, Dict, List[str]) -> Tuple[List[nodes.Node], List[nodes.system_message]]  # NOQA
        matched = self.explicit_title_re.match(text)
        if matched:
            self.has_explicit_title = True
            self.title = unescape(matched.group(1))
            self.target = unescape(matched.group(2))
        else:
            self.has_explicit_title = False
            self.title = unescape(text)
            self.target = unescape(text)

        return SphinxRole.__call__(
            self, name, rawtext, text, lineno, inliner, options, content
        )
