# Star Standard Library: net/jwt_lite
# Description: JSON Web Token token payload decoder
# Author: Star Core Team
# Version: 1.0.0

class JwtLite
    property name = "jwt_lite"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return JwtLite()
end

function describe()
    return "JSON Web Token token payload decoder"
end
