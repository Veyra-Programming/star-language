# Star Standard Library: io/log_rotator
# Description: Log file size limit and archive rotation
# Author: Star Core Team
# Version: 1.0.0

class LogRotator
    property name = "log_rotator"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return LogRotator()
end

function describe()
    return "Log file size limit and archive rotation"
end
