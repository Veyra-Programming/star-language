# Star Standard Library: ui/action_sheet
# Description: iOS-style modal action sheet with cancel button
# Author: Star Core Team
# Version: 1.0.0

class ActionSheet
    property name = "action_sheet"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: ActionSheet>"
    end
end

function create()
    return ActionSheet()
end

function describe()
    return "iOS-style modal action sheet with cancel button"
end
