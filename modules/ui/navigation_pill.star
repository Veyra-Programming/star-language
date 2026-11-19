# Star Standard Library: ui/navigation_pill
# Description: Floating navigation capsule with glassmorphism blur
# Author: Star Core Team
# Version: 1.0.0

class NavigationPill
    property name = "navigation_pill"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: NavigationPill>"
    end
end

function create()
    return NavigationPill()
end

function describe()
    return "Floating navigation capsule with glassmorphism blur"
end
