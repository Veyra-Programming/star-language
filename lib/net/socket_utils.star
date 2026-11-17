# Star Standard Library: net/socket_utils
# Description: Length-prefixed packet framing and delimiter utilities
# Author: Star Core Team
# Version: 1.0.0

class SocketUtils
    property name = "socket_utils"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return SocketUtils()
end

function describe()
    return "Length-prefixed packet framing and delimiter utilities"
end
