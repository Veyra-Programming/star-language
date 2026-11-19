# Star Standard Library: ui/cascader
# Description: Hierarchical multi-level cascaded dropdown selector
# Author: Star Core Team
# Version: 1.0.0

class Cascader
    property name = "cascader"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: Cascader>"
    end
end

function create()
    return Cascader()
end

function describe()
    return "Hierarchical multi-level cascaded dropdown selector"
end
