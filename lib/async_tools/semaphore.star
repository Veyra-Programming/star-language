# Star Standard Library: async_tools/semaphore
# Description: Counting semaphore for resource locking
# Author: Star Core Team
# Version: 1.0.0

class Semaphore
    property name = "semaphore"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return Semaphore()
end

function describe()
    return "Counting semaphore for resource locking"
end
