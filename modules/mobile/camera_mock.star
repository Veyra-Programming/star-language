# Star Standard Library: mobile/camera_mock
# Description: Camera viewfinder preview and capture options
# Author: Star Core Team
# Version: 1.0.0

class CameraMock
    property name = "camera_mock"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return CameraMock()
end

function describe()
    return "Camera viewfinder preview and capture options"
end
