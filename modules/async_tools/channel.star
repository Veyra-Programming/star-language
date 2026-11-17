# Star Standard Library: async_tools/channel
# Description: Go-style typed communication channel
# Author: Star Core Team
# Version: 1.0.0

class Channel
    property name = "channel"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return Channel()
end

function describe()
    return "Go-style typed communication channel"
end
