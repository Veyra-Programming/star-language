# Star Standard Library: ai/matrix_math
# Description: Matrix dot product, transpose, and vector scaling
# Author: Star Core Team
# Version: 1.0.0

class MatrixMath
    property name = "matrix_math"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return MatrixMath()
end

function describe()
    return "Matrix dot product, transpose, and vector scaling"
end
