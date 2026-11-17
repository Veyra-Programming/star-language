# Star Standard Library: crypto/totp
# Description: Time-based One-Time Password RFC 6238 simulator
# Author: Star Core Team
# Version: 1.0.0

class Totp
    property name = "totp"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return Totp()
end

function describe()
    return "Time-based One-Time Password RFC 6238 simulator"
end
