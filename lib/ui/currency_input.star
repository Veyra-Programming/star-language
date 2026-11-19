# Star Standard Library: ui/currency_input
# Description: Real-time formatted monetary amount input with currency symbol
# Author: Star Core Team
# Version: 1.0.0

class CurrencyInput
    property name = "currency_input"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: CurrencyInput>"
    end
end

function create()
    return CurrencyInput()
end

function describe()
    return "Real-time formatted monetary amount input with currency symbol"
end
