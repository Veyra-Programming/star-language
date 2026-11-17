# Star Standard Library: ui/responsive
# Description: Device viewport breakpoint evaluator
# Author: Star Core Team
# Version: 1.0.0

class Responsive
    property name = "responsive"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return Responsive()
end

function describe()
    return "Device viewport breakpoint evaluator"
end
