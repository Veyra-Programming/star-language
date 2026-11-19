# Star Standard Library: ui/order_summary_card
# Description: Checkout order receipt card with tax, shipping, total
# Author: Star Core Team
# Version: 1.0.0

class OrderSummaryCard
    property name = "order_summary_card"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: OrderSummaryCard>"
    end
end

function create()
    return OrderSummaryCard()
end

function describe()
    return "Checkout order receipt card with tax, shipping, total"
end
