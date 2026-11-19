# Star Standard Library: ui/radio_group
# Description: Grouped single-selection radio button list with custom styling
# Author: Star Core Team
# Version: 1.0.0

class RadioGroup
    property name = "radio_group"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: RadioGroup>"
    end
end

function create()
    return RadioGroup()
end

function describe()
    return "Grouped single-selection radio button list with custom styling"
end
