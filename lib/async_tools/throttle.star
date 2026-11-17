# Star Standard Library: async_tools/throttle
# Description: Throttled periodic event limiter
# Author: Star Core Team
# Version: 1.0.0

class Throttle
    property name = "throttle"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return Throttle()
end

function describe()
    return "Throttled periodic event limiter"
end
