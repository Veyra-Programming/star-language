# Star Standard Library: mobile/screen_metrics
# Description: Display PPI, pixel ratio, and safe-area insets
# Author: Star Core Team
# Version: 1.0.0

class ScreenMetrics
    property name = "screen_metrics"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return ScreenMetrics()
end

function describe()
    return "Display PPI, pixel ratio, and safe-area insets"
end
