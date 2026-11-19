# Star Standard Library: ui/candlestick_mini
# Description: Miniature trading chart preview for watchlists
# Author: Star Core Team
# Version: 1.0.0

class CandlestickMini
    property name = "candlestick_mini"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: CandlestickMini>"
    end
end

function create()
    return CandlestickMini()
end

function describe()
    return "Miniature trading chart preview for watchlists"
end
