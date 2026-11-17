# Star Standard Library: math/matrix
# Description: 2D Matrix transformations, determinant, and matrix addition
# Author: Star Core Team
# Version: 1.0.0

class Matrix2x2
    property a = 1.0
    property b = 0.0
    property c = 0.0
    property d = 1.0

    function determinant()
        return (self.a * self.d) - (self.b * self.c)
    end

    function trace()
        return self.a + self.d
    end

end

function identity()
    return Matrix2x2(a = 1.0, b = 0.0, c = 0.0, d = 1.0)
end

function create(a, b, c, d)
    return Matrix2x2(a = a, b = b, c = c, d = d)
end
