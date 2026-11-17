# Star Standard Library: crypto/xtea
# Description: XTEA 64-bit block cipher 32-round implementation
# Author: Star Core Team
# Version: 1.0.0

class Xtea
    property name = "xtea"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return Xtea()
end

function describe()
    return "XTEA 64-bit block cipher 32-round implementation"
end
