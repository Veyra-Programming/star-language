# Star Standard Library: algorithms/searching
# Description: Binary search, linear search, and lookup bounds
# Author: Star Core Team
# Version: 1.0.0

class Searching
    property name = "searching"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return Searching()
end

function describe()
    return "Binary search, linear search, and lookup bounds"
end
