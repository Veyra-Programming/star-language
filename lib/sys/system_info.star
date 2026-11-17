# Star Standard Library: sys/system_info
# Description: Host OS, processor architecture, and core counts
# Author: Star Core Team
# Version: 1.0.0

class SystemInfo
    property name = "system_info"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return SystemInfo()
end

function describe()
    return "Host OS, processor architecture, and core counts"
end
