# Star Standard Library: ui/code_snippet_card
# Description: Syntax-highlighted code snippet card with copy button
# Author: Star Core Team
# Version: 1.0.0

class CodeSnippetCard
    property name = "code_snippet_card"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: CodeSnippetCard>"
    end
end

function create()
    return CodeSnippetCard()
end

function describe()
    return "Syntax-highlighted code snippet card with copy button"
end
