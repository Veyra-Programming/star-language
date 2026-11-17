# Star Standard Library: mobile/device_info
# Description: Platform architecture, OS version, and device name
# Author: Star Core Team
# Version: 1.0.0

class DeviceInfo
    property name = "device_info"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return DeviceInfo()
end

function describe()
    return "Platform architecture, OS version, and device name"
end
