# Star Standard Library: ui/dropdown_select
# Description: Standard customizable dropdown picker with icons
# Author: Star Core Team
# Version: 1.0.0

class DropdownSelect
    property name = "dropdown_select"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: DropdownSelect>"
    end
end

function create()
    return DropdownSelect()
end

function describe()
    return "Standard customizable dropdown picker with icons"
end
