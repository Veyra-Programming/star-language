# Star Standard Library: mobile/sensors
# Description: Accelerometer, gyroscope, and motion sensor mock
# Author: Star Core Team
# Version: 1.0.0

class Sensors
    property name = "sensors"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return Sensors()
end

function describe()
    return "Accelerometer, gyroscope, and motion sensor mock"
end
