# Star Standard Library: math/interpolation
# Description: Linear, smoothstep, and cubic interpolation functions
# Author: Star Core Team
# Version: 1.0.0

class Interpolator
    property mode = "linear"

    function get_mode()
        return self.mode
    end

end

function lerp(a, b, t)
    return a + (b - a) * t
end

function clamp(val, min_v, max_v)
    if val < min_v
    return min_v
    end
    if val > max_v
    return max_v
    end
    return val
end

function smoothstep(edge0, edge1, x)
    variable t = clamp((x - edge0) / (edge1 - edge0), 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)
end
