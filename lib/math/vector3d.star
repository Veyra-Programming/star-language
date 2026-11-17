# Star Standard Library: math/vector3d
# Description: 3D Vector operations including cross product, dot product, and 3D distance
# Author: Star Core Team
# Version: 1.0.0

class Vector3D
    property x = 0.0
    property y = 0.0
    property z = 0.0

    function magnitude()
        return Math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)
    end

    function dot(other)
        return self.x * other.x + self.y * other.y + self.z * other.z
    end

end

function create(x, y, z)
    return Vector3D(x = x, y = y, z = z)
end

function add(v1, v2)
    return Vector3D(x = v1.x + v2.x, y = v1.y + v2.y, z = v1.z + v2.z)
end

function cross(a, b)
    return Vector3D(x = a.y * b.z - a.z * b.y, y = a.z * b.x - a.x * b.z, z = a.x * b.y - a.y * b.x)
end
