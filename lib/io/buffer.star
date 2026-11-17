# Star Standard Library: io/buffer
# Description: Byte buffer byte manipulation and hex slicing
# Author: Star Core Team
# Version: 1.0.0

class Buffer
    property name = "buffer"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return Buffer()
end

function describe()
    return "Byte buffer byte manipulation and hex slicing"
end
