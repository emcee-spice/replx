"""TO-DO: Write a description of what this XBlock is."""

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

    editor_text = String(
        default=EDITOR_DEFAULT,
        scope=Scope.user_state,
        help="Text within the code editor."
    )

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    # TO-DO: change this view to display your data your own way.
    def student_view(self, context=None):
        """
        The primary view of the ReplXBlock, shown to students
        when viewing courses.
        """
        html = self.resource_string("static/html/replx.html")
        frag = Fragment(html.format(self=self))
        frag.add_css(self.resource_string("static/css/replx.css"))
        frag.add_css(self.resource_string("static/css/codemirror.css"))
        frag.add_css(self.resource_string("static/css/codemirror-repl.css"))
        frag.add_javascript(self.resource_string("static/js/lib/codemirror/codemirror-repl.min.js"))
        frag.add_javascript(self.resource_string("static/js/lib/codemirror/codemirror.min.js"))
        frag.add_javascript(self.resource_string("static/js/lib/skulpt/skulpt.min.js"))
        frag.add_javascript(self.resource_string("static/js/lib/skulpt/skulpt-stdlib.js"))
        frag.add_javascript(self.resource_string("static/js/src/replx.js"))
        frag.add_javascript(self.resource_string("static/js/src/python-repl.js"))
        frag.initialize_js('ReplXBlock')
        return frag

    @XBlock.json_handler
    def save_editor_text(self, data, suffix=''):  # pylint: disable=unused-argument
        """
        Save the text in the code editor.
        """
        self.editor_text = data["editorText"]
        return {}  # TODO: is this necessary?

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
