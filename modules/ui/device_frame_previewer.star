# Star Standard Library: ui/device_frame_previewer
# Description: Realistic iPhone, iPad, Android, and MacBook device mockups
# Author: Star Core Team
# Version: 1.0.0

class DeviceFramePreviewer
    property name = "device_frame_previewer"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: DeviceFramePreviewer>"
    end
end

function create()
    return DeviceFramePreviewer()
end

function describe()
    return "Realistic iPhone, iPad, Android, and MacBook device mockups"
end
