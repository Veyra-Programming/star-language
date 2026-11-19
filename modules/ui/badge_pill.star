# Star Standard Library: ui/badge_pill
# Description: Notification counter and status tag badge with dot variant
# Author: Star Core Team
# Version: 1.0.0

class BadgePill
    property name = "badge_pill"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: BadgePill>"
    end
end

function create()
    return BadgePill()
end

function describe()
    return "Notification counter and status tag badge with dot variant"
end
