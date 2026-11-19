# Star Standard Library: ui/meter_bar
# Description: Hardware storage and battery meter bar with critical levels
# Author: Star Core Team
# Version: 1.0.0

class MeterBar
    property name = "meter_bar"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: MeterBar>"
    end
end

function create()
    return MeterBar()
end

function describe()
    return "Hardware storage and battery meter bar with critical levels"
end
