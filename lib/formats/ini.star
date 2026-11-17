# Star Standard Library: formats/ini
# Description: INI file section and property parser
# Author: Star Core Team
# Version: 1.0.0

class Ini
    property name = "ini"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return Ini()
end

function describe()
    return "INI file section and property parser"
end
