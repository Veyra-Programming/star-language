# Star Standard Library: ui/rich_text_editor
# Description: WYSIWYG formatted text editor with bold, italic, lists
# Author: Star Core Team
# Version: 1.0.0

class RichTextEditor
    property name = "rich_text_editor"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: RichTextEditor>"
    end
end

function create()
    return RichTextEditor()
end

function describe()
    return "WYSIWYG formatted text editor with bold, italic, lists"
end
