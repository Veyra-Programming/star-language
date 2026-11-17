# Star Standard Library: mobile/shake_detector
# Description: Device shake motion gesture detector
# Author: Star Core Team
# Version: 1.0.0

class ShakeDetector
    property name = "shake_detector"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return ShakeDetector()
end

function describe()
    return "Device shake motion gesture detector"
end
