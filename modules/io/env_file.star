# Star Standard Library: io/env_file
# Description: .env configuration file parser
# Author: Star Core Team
# Version: 1.0.0

class EnvFile
    property name = "env_file"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return EnvFile()
end

function describe()
    return ".env configuration file parser"
end
