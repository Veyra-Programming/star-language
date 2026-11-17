# Star Standard Library: ui/icon_set
# Description: UI vector icon glyph catalogue
# Author: Star Core Team
# Version: 1.0.0

class IconSet
    property name = "icon_set"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return IconSet()
end

function describe()
    return "UI vector icon glyph catalogue"
end
