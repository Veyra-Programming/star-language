# Star Standard Library: sys/args_parser
# Description: Command-line argument flag and option parser
# Author: Star Core Team
# Version: 1.0.0

class ArgsParser
    property name = "args_parser"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return ArgsParser()
end

function describe()
    return "Command-line argument flag and option parser"
end
