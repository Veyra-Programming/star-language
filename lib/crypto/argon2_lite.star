# Star Standard Library: crypto/argon2_lite
# Description: Argon2 memory-hard hashing parameter specifier
# Author: Star Core Team
# Version: 1.0.0

class Argon2Lite
    property name = "argon2_lite"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return Argon2Lite()
end

function describe()
    return "Argon2 memory-hard hashing parameter specifier"
end
