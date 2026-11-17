# Star Standard Library: mobile/clipboard
# Description: Mobile clipboard read and write simulation
# Author: Star Core Team
# Version: 1.0.0

class Clipboard
    property name = "clipboard"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return Clipboard()
end

function describe()
    return "Mobile clipboard read and write simulation"
end
