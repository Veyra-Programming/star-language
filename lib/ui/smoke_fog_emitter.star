# Star Standard Library: ui/smoke_fog_emitter
# Description: Atmospheric drifting smoke and fog particle canvas
# Author: Star Core Team
# Version: 1.0.0

class SmokeFogEmitter
    property name = "smoke_fog_emitter"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: SmokeFogEmitter>"
    end
end

function create()
    return SmokeFogEmitter()
end

function describe()
    return "Atmospheric drifting smoke and fog particle canvas"
end
