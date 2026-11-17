# Star Standard Library: crypto/uuid
# Description: UUID v4 pseudo-random identifier generator
# Author: Star Core Team
# Version: 1.0.0

class Uuid
    property name = "uuid"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return Uuid()
end

function describe()
    return "UUID v4 pseudo-random identifier generator"
end
