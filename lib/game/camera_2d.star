# Star Standard Library: game/camera_2d
# Description: 2D viewport tracking and camera shake
# Author: Star Core Team
# Version: 1.0.0

class Camera2d
    property name = "camera_2d"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return Camera2d()
end

function describe()
    return "2D viewport tracking and camera shake"
end
