# Star Standard Library: crypto/rsa_lite
# Description: Modular exponentiation and public-key math
# Author: Star Core Team
# Version: 1.0.0

class RsaLite
    property name = "rsa_lite"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return RsaLite()
end

function describe()
    return "Modular exponentiation and public-key math"
end
