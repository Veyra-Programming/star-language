# Star Standard Library: ui/activity_gauge
# Description: Apple Watch-style concentric circular fitness rings
# Author: Star Core Team
# Version: 1.0.0

class ActivityGauge
    property name = "activity_gauge"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: ActivityGauge>"
    end
end

function create()
    return ActivityGauge()
end

function describe()
    return "Apple Watch-style concentric circular fitness rings"
end
