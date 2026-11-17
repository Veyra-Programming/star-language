# Star Standard Library: math/linear_algebra
# Description: Linear algebra operations, dot products, vector projections, and norms
# Author: Star Core Team
# Version: 1.0.0

class LinearSpace
    property dimension = 2

    function dim()
        return self.dimension
    end

end

function dot_product_2d(x1, y1, x2, y2)
    return x1 * x2 + y1 * y2
end

function vector_length_2d(x, y)
    return Math.sqrt(x * x + y * y)
end

function project_scalar(x1, y1, x2, y2)
    variable dot = x1 * x2 + y1 * y2
    variable len_sq = x2 * x2 + y2 * y2
    if len_sq == 0
    return 0.0
    end
    return dot / len_sq
end
