# Star Standard Library: sys/time_utils
# Description: Epoch timestamps, duration formatting, and dates
# Author: Star Core Team
# Version: 1.0.0

class TimeUtils
    property name = "time_utils"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return TimeUtils()
end

function describe()
    return "Epoch timestamps, duration formatting, and dates"
end
