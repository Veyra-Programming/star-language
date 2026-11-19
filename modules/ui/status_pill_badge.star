# Star Standard Library: ui/status_pill_badge
# Description: Rounded status indicator with animated pulsing dot
# Author: Star Core Team
# Version: 1.0.0

class StatusPillBadge
    property name = "status_pill_badge"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: StatusPillBadge>"
    end
end

function create()
    return StatusPillBadge()
end

function describe()
    return "Rounded status indicator with animated pulsing dot"
end
