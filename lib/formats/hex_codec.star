# Star Standard Library: formats/hex_codec
# Description: Hexadecimal string and byte converter
# Author: Star Core Team
# Version: 1.0.0

class HexCodec
    property name = "hex_codec"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return HexCodec()
end

function describe()
    return "Hexadecimal string and byte converter"
end
