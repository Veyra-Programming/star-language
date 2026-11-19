# Star Standard Library: ui/markdown_editor
# Description: Split-pane markdown source editor with live preview
# Author: Star Core Team
# Version: 1.0.0

class MarkdownEditor
    property name = "markdown_editor"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: MarkdownEditor>"
    end
end

function create()
    return MarkdownEditor()
end

function describe()
    return "Split-pane markdown source editor with live preview"
end
