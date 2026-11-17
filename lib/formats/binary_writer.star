# Star Standard Library: formats/binary_writer
# Description: Binary buffer writer for serialized bytes
# Author: Star Core Team
# Version: 1.0.0

class BinaryWriter
    property name = "binary_writer"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return BinaryWriter()
end

function describe()
    return "Binary buffer writer for serialized bytes"
end
