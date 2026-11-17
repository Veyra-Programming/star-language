# Star Standard Library: ui/typography
# Description: Type scale, line height, and font hierarchy
# Author: Star Core Team
# Version: 1.0.0

class Typography
    property name = "typography"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return Typography()
end

function describe()
    return "Type scale, line height, and font hierarchy"
end
