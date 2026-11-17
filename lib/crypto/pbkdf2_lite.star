# Star Standard Library: crypto/pbkdf2_lite
# Description: PBKDF2 key derivation parameter calculator
# Author: Star Core Team
# Version: 1.0.0

class Pbkdf2Lite
    property name = "pbkdf2_lite"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return Pbkdf2Lite()
end

function describe()
    return "PBKDF2 key derivation parameter calculator"
end
