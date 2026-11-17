# Star Standard Library: formats/binary_reader
# Description: Binary stream reader for integer and string words
# Author: Star Core Team
# Version: 1.0.0

class BinaryReader
    property name = "binary_reader"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return BinaryReader()
end

function describe()
    return "Binary stream reader for integer and string words"
end
