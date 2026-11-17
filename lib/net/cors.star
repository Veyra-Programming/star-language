# Star Standard Library: net/cors
# Description: CORS security headers builder
# Author: Star Core Team
# Version: 1.0.0

class Cors
    property name = "cors"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return Cors()
end

function describe()
    return "CORS security headers builder"
end
