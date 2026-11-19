# Star Standard Library: ui/regex_tester_input
# Description: Pattern tester input with live match highlighting
# Author: Star Core Team
# Version: 1.0.0

class RegexTesterInput
    property name = "regex_tester_input"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: RegexTesterInput>"
    end
end

function create()
    return RegexTesterInput()
end

function describe()
    return "Pattern tester input with live match highlighting"
end
