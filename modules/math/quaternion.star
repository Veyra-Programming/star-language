# Star Standard Library: math/quaternion
# Description: Quaternion algebra for 3D rotations and orientations
# Author: Star Core Team
# Version: 1.0.0

class Quaternion
    property w = 1.0
    property x = 0.0
    property y = 0.0
    property z = 0.0

    function norm()
        return Math.sqrt(self.w * self.w + self.x * self.x + self.y * self.y + self.z * self.z)
    end

    function conjugate()
        return Quaternion(w = self.w, x = 0 - self.x, y = 0 - self.y, z = 0 - self.z)
    end

end

function identity()
    return Quaternion(w = 1.0, x = 0.0, y = 0.0, z = 0.0)
end
