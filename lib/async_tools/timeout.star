# Star Standard Library: async_tools/timeout
# Description: Async operation timeout and cancellation guard
# Author: Star Core Team
# Version: 1.0.0

class Timeout
    property name = "timeout"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return Timeout()
end

function describe()
    return "Async operation timeout and cancellation guard"
end
