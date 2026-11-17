# Star Standard Library: game/raycast_2d
# Description: 2D line and ray-box intersection testing
# Author: Star Core Team
# Version: 1.0.0

class Raycast2d
    property name = "raycast_2d"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return Raycast2d()
end

function describe()
    return "2D line and ray-box intersection testing"
end
