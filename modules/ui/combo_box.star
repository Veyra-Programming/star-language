# Star Standard Library: ui/combo_box
# Description: Hybrid text input and dropdown select combo box
# Author: Star Core Team
# Version: 1.0.0

class ComboBox
    property name = "combo_box"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: ComboBox>"
    end
end

function create()
    return ComboBox()
end

function describe()
    return "Hybrid text input and dropdown select combo box"
end
