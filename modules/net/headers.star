# Star Standard Library: net/headers
# Description: HTTP header normalization and lookup map
# Author: Star Core Team
# Version: 1.0.0

class Headers
    property name = "headers"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return Headers()
end

function describe()
    return "HTTP header normalization and lookup map"
end
