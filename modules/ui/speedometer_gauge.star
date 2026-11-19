# Star Standard Library: ui/speedometer_gauge
# Description: Automotive-style high-precision dial speedometer
# Author: Star Core Team
# Version: 1.0.0

class SpeedometerGauge
    property name = "speedometer_gauge"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: SpeedometerGauge>"
    end
end

function create()
    return SpeedometerGauge()
end

function describe()
    return "Automotive-style high-precision dial speedometer"
end
