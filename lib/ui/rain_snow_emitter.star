# Star Standard Library: ui/rain_snow_emitter
# Description: Weather rain and snowfall particle effect overlay
# Author: Star Core Team
# Version: 1.0.0

class RainSnowEmitter
    property name = "rain_snow_emitter"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: RainSnowEmitter>"
    end
end

function create()
    return RainSnowEmitter()
end

function describe()
    return "Weather rain and snowfall particle effect overlay"
end
