# Star Standard Library: ui/badge
# Description: Status indicator and notification counter badge
# Author: Star Core Team
# Version: 1.0.0

class Badge
    property name = "badge"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return Badge()
end

function describe()
    return "Status indicator and notification counter badge"
end
