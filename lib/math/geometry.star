# Star Standard Library: math/geometry
# Description: 2D Geometric shapes, area, perimeter, and bounding box checks
# Author: Star Core Team
# Version: 1.0.0

class Rectangle
    property width = 0.0
    property height = 0.0

    function area()
        return self.width * self.height
    end

    function perimeter()
        return 2.0 * (self.width + self.height)
    end

end

function circle_area(radius)
    return 3.141592653589793 * radius * radius
end

function circle_circumference(radius)
    return 2.0 * 3.141592653589793 * radius
end

function point_in_rect(px, py, rx, ry, rw, rh)
    return px >= rx and px <= rx + rw and py >= ry and py <= ry + rh
end
