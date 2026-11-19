# Star Standard Library: ui/parallax_view
# Description: Multi-layer depth parallax scroll container
# Author: Star Core Team
# Version: 1.0.0

class ParallaxView
    property name = "parallax_view"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: ParallaxView>"
    end
end

function create()
    return ParallaxView()
end

function describe()
    return "Multi-layer depth parallax scroll container"
end
