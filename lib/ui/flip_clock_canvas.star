# Star Standard Library: ui/flip_clock_canvas
# Description: Vintage mechanical split-flap display for time/stats
# Author: Star Core Team
# Version: 1.0.0

class FlipClockCanvas
    property name = "flip_clock_canvas"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: FlipClockCanvas>"
    end
end

function create()
    return FlipClockCanvas()
end

function describe()
    return "Vintage mechanical split-flap display for time/stats"
end
