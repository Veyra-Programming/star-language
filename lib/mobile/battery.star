# Star Standard Library: mobile/battery
# Description: Battery level and power state monitor
# Author: Star Core Team
# Version: 1.0.0

class Battery
    property name = "battery"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return Battery()
end

function describe()
    return "Battery level and power state monitor"
end
