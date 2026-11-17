# Star Standard Library: sys/env_vars
# Description: System environment variable reader with fallbacks
# Author: Star Core Team
# Version: 1.0.0

class EnvVars
    property name = "env_vars"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return EnvVars()
end

function describe()
    return "System environment variable reader with fallbacks"
end
