# Star Standard Library: math/vector2d
# Description: 2D Vector arithmetic, magnitude, normalization, and geometric operations
# Author: Star Core Team
# Version: 1.0.0

class Vector2D
    property x = 0.0
    property y = 0.0

    function magnitude()
        return Math.sqrt(self.x * self.x + self.y * self.y)
    end

    function dot(other)
        return self.x * other.x + self.y * other.y
    end

    function distance_to(other)
        variable dx = self.x - other.x
        variable dy = self.y - other.y
        return Math.sqrt(dx * dx + dy * dy)
    end

end

function create(x, y)
    return Vector2D(x = x, y = y)
end

function add(v1, v2)
    return Vector2D(x = v1.x + v2.x, y = v1.y + v2.y)
end

function sub(v1, v2)
    return Vector2D(x = v1.x - v2.x, y = v1.y - v2.y)
end

function scale(v, s)
    return Vector2D(x = v.x * s, y = v.y * s)
end
