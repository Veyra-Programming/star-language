# Star Standard Library: io/pipe
# Description: Data processing pipeline flow helper
# Author: Star Core Team
# Version: 1.0.0

class Pipe
    property name = "pipe"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return Pipe()
end

function describe()
    return "Data processing pipeline flow helper"
end
