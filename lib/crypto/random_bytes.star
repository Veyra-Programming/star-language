# Star Standard Library: crypto/random_bytes
# Description: Cryptographically sound byte array generator
# Author: Star Core Team
# Version: 1.0.0

class RandomBytes
    property name = "random_bytes"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return RandomBytes()
end

function describe()
    return "Cryptographically sound byte array generator"
end
