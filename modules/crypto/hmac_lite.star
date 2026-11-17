# Star Standard Library: crypto/hmac_lite
# Description: HMAC key authentication helper
# Author: Star Core Team
# Version: 1.0.0

class HmacLite
    property name = "hmac_lite"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return HmacLite()
end

function describe()
    return "HMAC key authentication helper"
end
