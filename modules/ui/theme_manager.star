# Star Standard Library: ui/theme_manager
# Description: Dark and light theme styling dictionary
# Author: Star Core Team
# Version: 1.0.0

class ThemeManager
    property name = "theme_manager"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return ThemeManager()
end

function describe()
    return "Dark and light theme styling dictionary"
end
