# Star Standard Library: ui/pulse_indicator
# Description: Glowing radar pulse dot indicator for live updates
# Author: Star Core Team
# Version: 1.0.0

class PulseIndicator
    property name = "pulse_indicator"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: PulseIndicator>"
    end
end

function create()
    return PulseIndicator()
end

function describe()
    return "Glowing radar pulse dot indicator for live updates"
end
