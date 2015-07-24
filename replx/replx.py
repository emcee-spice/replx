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
        default=None,
        scope=Scope.user_state,
        help="Text within the code editor."
    )
    
    prerun_code = String(
        default="",
        scope=Scope.settings,
        help="Code to run before evaluating student code"
    )

    postrun_code = String(
        default="",
        scope=Scope.settings,
        help="Code to run after evaluating student code"
    )

    instructions = String(
        default="Enter your code below",
        scope=Scope.settings,
        help="Tell the student what to do with the code editor"
    )

    initial_code = String(
        default="",
        scope=Scope.settings,
        help="Initial code when the block is first loaded"
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
            'themeName': self._theme_name,
            'prerun_code': self.prerun_code,
            'postrun_code': self.postrun_code
        }
        self._params_json = json.dumps(self._params)

        if not self.editor_text:
            self.editor_text = self.initial_code

        # Dynamic assets
        self._theme_options = self._make_theme_options()
        html = self.resource_string("static/html/replx.html")
        frag = Fragment(html.format(self=self))
        frag.add_css(self._get_theme_css(self._theme_name))

        # Static assets
        frag.add_css(self.resource_string("static/css/codemirror.css"))
        frag.add_css(self.resource_string("static/css/replx.css"))
        frag.add_javascript(self.resource_string("static/js/lib/skulpt/skulpt.min.js"))
        frag.add_javascript(self.resource_string("static/js/lib/skulpt/skulpt-stdlib.min.js"))
        frag.add_javascript(self.resource_string("static/js/lib/codemirror/codemirror.js"))
        frag.add_javascript(self.resource_string("static/js/lib/codemirror/codemirror-repl.js"))
        frag.add_javascript(self.resource_string("static/js/lib/codemirror/python-syntax-mode.js"))
        frag.add_javascript(self.resource_string("static/js/src/python-repl.js"))
        frag.add_javascript(self.resource_string("static/js/src/replx.js"))

        # Misc
        frag.initialize_js('ReplXBlock')
        return frag

    def studio_view(self, context=None):
        html_str = self.resource_string("static/html/studio.html")
        frag = Fragment(html_str.format(self=self))
        frag.add_javascript(self.resource_string("static/js/src/replx-edit.js"))
        frag.initialize_js("ReplXBlockEdit")

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

    @XBlock.json_handler
    def studio_submit(self, data, suffix=''):
        """
        Called when submitting the form in Studio.
        """
        self.instructions = data.get('instructions')
        self.initial_code = data.get('initialcode')
        self.prerun_code = data.get('preruncode')
        self.postrun_code = data.get('postruncode')

        return {'result': 'success'}

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
