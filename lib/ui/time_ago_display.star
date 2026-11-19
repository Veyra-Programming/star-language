# Star Standard Library: ui/time_ago_display
# Description: Relative '5 minutes ago' reactive timestamp display
# Author: Star Core Team
# Version: 1.0.0

class TimeAgoDisplay
    property name = "time_ago_display"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: TimeAgoDisplay>"
    end
end

function create()
    return TimeAgoDisplay()
end

function describe()
    return "Relative '5 minutes ago' reactive timestamp display"
end
