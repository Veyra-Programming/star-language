# Star Standard Library: crypto/checksum
# Description: CRC32 and Adler32 checksum calculators
# Author: Star Core Team
# Version: 1.0.0

class Checksum
    property name = "checksum"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return Checksum()
end

function describe()
    return "CRC32 and Adler32 checksum calculators"
end
