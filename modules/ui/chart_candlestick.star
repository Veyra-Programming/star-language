# Star Standard Library: ui/chart_candlestick
# Description: Financial stock candlestick chart with high/low/open/close
# Author: Star Core Team
# Version: 1.0.0

class ChartCandlestick
    property name = "chart_candlestick"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: ChartCandlestick>"
    end
end

function create()
    return ChartCandlestick()
end

function describe()
    return "Financial stock candlestick chart with high/low/open/close"
end
