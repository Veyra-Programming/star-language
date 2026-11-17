# Star Standard Library: async_tools/promise
# Description: Promise state machine with resolve, reject, then
# Author: Star Core Team
# Version: 1.0.0

class Promise
    property name = "promise"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return Promise()
end

function describe()
    return "Promise state machine with resolve, reject, then"
end
