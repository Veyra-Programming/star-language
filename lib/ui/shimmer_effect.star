# Star Standard Library: ui/shimmer_effect
# Description: Moving gradient shimmer highlight for loading states
# Author: Star Core Team
# Version: 1.0.0

class ShimmerEffect
    property name = "shimmer_effect"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: ShimmerEffect>"
    end
end

function create()
    return ShimmerEffect()
end

function describe()
    return "Moving gradient shimmer highlight for loading states"
end
