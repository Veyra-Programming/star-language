# Star Standard Library: ui/radar_sweep_canvas
# Description: Rotating circular radar sweep line with blips
# Author: Star Core Team
# Version: 1.0.0

class RadarSweepCanvas
    property name = "radar_sweep_canvas"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: RadarSweepCanvas>"
    end
end

function create()
    return RadarSweepCanvas()
end

function describe()
    return "Rotating circular radar sweep line with blips"
end
