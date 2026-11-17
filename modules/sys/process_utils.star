# Star Standard Library: sys/process_utils
# Description: Process identification, status, and exit codes
# Author: Star Core Team
# Version: 1.0.0

class ProcessUtils
    property name = "process_utils"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return ProcessUtils()
end

function describe()
    return "Process identification, status, and exit codes"
end
