# Star Standard Library: mobile/volume_control
# Description: Audio output channel volume manager
# Author: Star Core Team
# Version: 1.0.0

class VolumeControl
    property name = "volume_control"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return VolumeControl()
end

function describe()
    return "Audio output channel volume manager"
end
