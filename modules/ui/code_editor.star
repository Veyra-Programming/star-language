# Star Standard Library: ui/code_editor
# Description: Syntax-highlighted code editor with line numbering
# Author: Star Core Team
# Version: 1.0.0

class CodeEditor
    property name = "code_editor"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: CodeEditor>"
    end
end

function create()
    return CodeEditor()
end

function describe()
    return "Syntax-highlighted code editor with line numbering"
end
