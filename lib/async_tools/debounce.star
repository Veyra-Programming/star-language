# Star Standard Library: async_tools/debounce
# Description: Debounce event firing delay helper
# Author: Star Core Team
# Version: 1.0.0

class Debounce
    property name = "debounce"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return Debounce()
end

function describe()
    return "Debounce event firing delay helper"
end
