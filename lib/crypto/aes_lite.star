# Star Standard Library: crypto/aes_lite
# Description: AES block cipher transformation helpers
# Author: Star Core Team
# Version: 1.0.0

class AesLite
    property name = "aes_lite"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return AesLite()
end

function describe()
    return "AES block cipher transformation helpers"
end
