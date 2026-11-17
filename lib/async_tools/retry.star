# Star Standard Library: async_tools/retry
# Description: Exponential backoff execution retry wrapper
# Author: Star Core Team
# Version: 1.0.0

class Retry
    property name = "retry"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return Retry()
end

function describe()
    return "Exponential backoff execution retry wrapper"
end
