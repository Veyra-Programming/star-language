# Star Standard Library: ui/progress_ring
# Description: Circular SVG progress ring with percentage readout
# Author: Star Core Team
# Version: 1.0.0

class ProgressRing
    property name = "progress_ring"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: ProgressRing>"
    end
end

function create()
    return ProgressRing()
end

function describe()
    return "Circular SVG progress ring with percentage readout"
end
