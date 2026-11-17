# Star Standard Library: crypto/sha256_lite
# Description: SHA-256 block hashing primitives and padding
# Author: Star Core Team
# Version: 1.0.0

class Sha256Lite
    property name = "sha256_lite"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return Sha256Lite()
end

function describe()
    return "SHA-256 block hashing primitives and padding"
end
