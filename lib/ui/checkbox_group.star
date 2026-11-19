# Star Standard Library: ui/checkbox_group
# Description: Grouped tri-state checkbox list with select-all
# Author: Star Core Team
# Version: 1.0.0

class CheckboxGroup
    property name = "checkbox_group"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: CheckboxGroup>"
    end
end

function create()
    return CheckboxGroup()
end

function describe()
    return "Grouped tri-state checkbox list with select-all"
end
