# Star Standard Library: ui/gradient
# Description: Linear and radial CSS gradient generators
# Author: Star Core Team
# Version: 1.0.0

class Gradient
    property name = "gradient"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return Gradient()
end

function describe()
    return "Linear and radial CSS gradient generators"
end
