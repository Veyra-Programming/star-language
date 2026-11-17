# Star Standard Library: sys/terminal
# Description: Terminal dimension detection and cursor control
# Author: Star Core Team
# Version: 1.0.0

class Terminal
    property name = "terminal"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return Terminal()
end

function describe()
    return "Terminal dimension detection and cursor control"
end
