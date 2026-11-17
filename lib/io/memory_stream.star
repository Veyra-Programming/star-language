# Star Standard Library: io/memory_stream
# Description: In-memory binary stream
# Author: Star Core Team
# Version: 1.0.0

class MemoryStream
    property name = "memory_stream"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return MemoryStream()
end

function describe()
    return "In-memory binary stream"
end
