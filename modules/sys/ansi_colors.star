# Star Standard Library: sys/ansi_colors
# Description: ANSI 16-color and 256-color terminal escape codes
# Author: Star Core Team
# Version: 1.0.0

class AnsiColors
    property name = "ansi_colors"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return AnsiColors()
end

function describe()
    return "ANSI 16-color and 256-color terminal escape codes"
end
