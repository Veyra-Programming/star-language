# Star Standard Library: strings/base64_codec
# Description: Base64 encoding and decoding helpers
# Author: Star Core Team
# Version: 1.0.0

class Base64Codec
    property name = "base64_codec"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return Base64Codec()
end

function describe()
    return "Base64 encoding and decoding helpers"
end
