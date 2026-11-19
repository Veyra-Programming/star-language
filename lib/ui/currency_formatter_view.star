# Star Standard Library: ui/currency_formatter_view
# Description: International multi-currency live conversion display
# Author: Star Core Team
# Version: 1.0.0

class CurrencyFormatterView
    property name = "currency_formatter_view"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: CurrencyFormatterView>"
    end
end

function create()
    return CurrencyFormatterView()
end

function describe()
    return "International multi-currency live conversion display"
end
