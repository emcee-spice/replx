"""TO-DO: Write a description of what this XBlock is."""

import json
import pkg_resources

from xblock.core import XBlock
from xblock.fields import Scope, String
from xblock.fragment import Fragment


class ReplXBlock(XBlock):
    """
    TO-DO: document what your XBlock does.
    """

    EDITOR_DEFAULT = """
# You can edit your Python here.

def say_hello(name):
    print "Hello, " + name + "!"

say_hello("<your name here>")

"""

    AVAILABLE_THEMES = {
        'default',
        "3024-day",
        "3024-night",
        "ambiance",
        "base16-dark",
        "base16-light",
        "blackboard",
        "cobalt",
        "colorforth",
        "dracula",
        "eclipse",
        "elegant",
        "erlang-dark",
        "icecoder",
        "lesser-dark",
        "liquibyte",
        "material",
        "mbo",
        "mdn-like",
        "midnight",
        "monokai",
        "neat",
        "neo",
        "night",
        "paraiso-dark",
        "paraiso-light",
        "pastel-on-dark",
        "rubyblue",
        "seti",
        "solarized",
        "the-matrix",
        "tomorrow-night-bright",
        "tomorrow-night-eighties",
        "ttcn",
        "twilight",
        "vibrant-ink",
        "xq-dark",
        "xq-light",
        "yeti",
        "zenburn",
    }

    editor_text = String(
        default=EDITOR_DEFAULT,
        scope=Scope.user_state,
        help="Text within the code editor."
    )
    _theme_name = String(
        default='default',
        scope=Scope.preferences,
        help="Theme of the code editor."
    )

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    def _make_theme_options(self):
        return ''.join(
            '<option value="{}">{}</option>'.format(theme, theme.title().replace('-', ' '))
            for theme in self.AVAILABLE_THEMES
        )

    # TO-DO: change this view to display your data your own way.
    def student_view(self, context=None):
        """
        The primary view of the ReplXBlock, shown to students
        when viewing courses.
        """

        # Parameters
        self._params = {
            'themeName': self._theme_name
        }
        self._params_json = json.dumps(self._params)

        # Dynamic assets
        self._theme_options = self._make_theme_options()
        html = self.resource_string("static/html/replx.html")
        frag = Fragment(html.format(self=self))
        frag.add_css(self._get_theme_css(self._theme_name))

        # Static assets
        frag.add_css(self.resource_string("static/css/codemirror.css"))
        frag.add_css(self.resource_string("static/css/codemirror-repl.css"))
        frag.add_css(self.resource_string("static/css/replx.css"))
        frag.add_javascript(self.resource_string("static/js/lib/codemirror/codemirror_python.min.js"))
        frag.add_javascript(self.resource_string("static/js/lib/codemirror/codemirror-repl.min.js"))
        frag.add_javascript(self.resource_string("static/js/lib/skulpt/skulpt.min.js"))
        frag.add_javascript(self.resource_string("static/js/lib/skulpt/skulpt-stdlib.js"))
        frag.add_javascript(self.resource_string("static/js/src/python-repl.js"))
        frag.add_javascript(self.resource_string("static/js/src/replx.js"))

        # Misc
        frag.initialize_js('ReplXBlock')
        return frag

    @XBlock.json_handler
    def save_editor_text(self, data, suffix=''):  # pylint: disable=unused-argument
        """
        Save the text in the code editor.
        """
        self.editor_text = data["editorText"]
        return {}  # TODO: is this necessary?

    def _get_theme_css(self, themeName):
        """
        Arguments:
            themeName (str): If not in self.AVAILABLE_THEMES, becomes 'default'

        Returns:
            str: CSS required to display theme.
                If themeName == 'default', then an empty string is returned,
                because the CSS required to display that theme is in
                codemirror.min.js.
        """
        return (
            '' if themeName == 'default' or themeName not in self.AVAILABLE_THEMES
            else self.resource_string("static/css/themes/{}.css".format(themeName))
        )

    @XBlock.json_handler
    def change_theme(self, data, suffix=''):  # pylint: disable=unused-argument
        """
        Save the text in the code editor.
        """
        theme = data["themeName"]
        if theme in self.AVAILABLE_THEMES:
            self._theme_name = theme
            return {
                "themeCSS": self._get_theme_css(theme)
            }
        else:
            pass  # TODO: Handle errors.

    # TO-DO: change this to create the scenarios you'd like to see in the
    # workbench while developing your XBlock.
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("ReplXBlock",
             """<replx />
             """),
        ]
