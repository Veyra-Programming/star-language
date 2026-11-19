# Star Standard Library: ui/gl_viewport
# Description: WebGL / WebGPU 3D viewport canvas for shaders and meshes
# Author: Star Core Team
# Version: 1.0.0

class GlViewport
    property name = "gl_viewport"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: GlViewport>"
    end
end

function create()
    return GlViewport()
end

function describe()
    return "WebGL / WebGPU 3D viewport canvas for shaders and meshes"
end
