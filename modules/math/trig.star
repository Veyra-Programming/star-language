# Star Standard Library: math/trig
# Description: Trigonometric helpers, angle conversions, and hypotenuse calculations
# Author: Star Core Team
# Version: 1.0.0

class Angle
    property degrees = 0.0

    function to_radians()
        return self.degrees * 3.141592653589793 / 180.0
    end

end

function deg_to_rad(deg)
    return deg * 3.141592653589793 / 180.0
end

function rad_to_deg(rad)
    return rad * 180.0 / 3.141592653589793
end

function hypotenuse(a, b)
    return Math.sqrt(a * a + b * b)
end
