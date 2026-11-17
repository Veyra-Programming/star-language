# Star Standard Library: net/sse
# Description: Server-Sent Events message formatter
# Author: Star Core Team
# Version: 1.0.0

class Sse
    property name = "sse"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return Sse()
end

function describe()
    return "Server-Sent Events message formatter"
end
