# Star Standard Library: mobile/orientation
# Description: Device screen rotation and orientation lock
# Author: Star Core Team
# Version: 1.0.0

class Orientation
    property name = "orientation"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return Orientation()
end

function describe()
    return "Device screen rotation and orientation lock"
end
