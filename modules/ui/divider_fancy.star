# Star Standard Library: ui/divider_fancy
# Description: Decorative divider with centered text, icon, or gradient
# Author: Star Core Team
# Version: 1.0.0

class DividerFancy
    property name = "divider_fancy"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: DividerFancy>"
    end
end

function create()
    return DividerFancy()
end

function describe()
    return "Decorative divider with centered text, icon, or gradient"
end
