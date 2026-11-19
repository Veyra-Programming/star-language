# Star Standard Library: ui/badge_ribbon
# Description: Corner diagonal ribbon badge (New, Sale, Pro, Beta)
# Author: Star Core Team
# Version: 1.0.0

class BadgeRibbon
    property name = "badge_ribbon"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: BadgeRibbon>"
    end
end

function create()
    return BadgeRibbon()
end

function describe()
    return "Corner diagonal ribbon badge (New, Sale, Pro, Beta)"
end
