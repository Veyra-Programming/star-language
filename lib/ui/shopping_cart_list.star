# Star Standard Library: ui/shopping_cart_list
# Description: E-commerce shopping bag list with thumbnail, price, delete
# Author: Star Core Team
# Version: 1.0.0

class ShoppingCartList
    property name = "shopping_cart_list"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: ShoppingCartList>"
    end
end

function create()
    return ShoppingCartList()
end

function describe()
    return "E-commerce shopping bag list with thumbnail, price, delete"
end
