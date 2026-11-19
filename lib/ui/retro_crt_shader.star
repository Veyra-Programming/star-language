# Star Standard Library: ui/retro_crt_shader
# Description: Retro CRT monitor curvature and scanline overlay
# Author: Star Core Team
# Version: 1.0.0

class RetroCrtShader
    property name = "retro_crt_shader"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: RetroCrtShader>"
    end
end

function create()
    return RetroCrtShader()
end

function describe()
    return "Retro CRT monitor curvature and scanline overlay"
end
