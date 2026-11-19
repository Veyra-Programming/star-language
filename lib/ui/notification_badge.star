# Star Standard Library: ui/notification_badge
# Description: Animated bouncing notification badge with counter
# Author: Star Core Team
# Version: 1.0.0

class NotificationBadge
    property name = "notification_badge"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: NotificationBadge>"
    end
end

function create()
    return NotificationBadge()
end

function describe()
    return "Animated bouncing notification badge with counter"
end
