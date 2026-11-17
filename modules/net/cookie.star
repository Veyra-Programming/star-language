# Star Standard Library: net/cookie
# Description: HTTP Cookie parser and Set-Cookie serializer
# Author: Star Core Team
# Version: 1.0.0

class Cookie
    property name = "cookie"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return Cookie()
end

function describe()
    return "HTTP Cookie parser and Set-Cookie serializer"
end
