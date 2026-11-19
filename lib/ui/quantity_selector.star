# Star Standard Library: ui/quantity_selector
# Description: E-commerce shopping cart item quantity adjuster
# Author: Star Core Team
# Version: 1.0.0

class QuantitySelector
    property name = "quantity_selector"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: QuantitySelector>"
    end
end

function create()
    return QuantitySelector()
end

function describe()
    return "E-commerce shopping cart item quantity adjuster"
end
