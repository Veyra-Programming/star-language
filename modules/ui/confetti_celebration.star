# Star Standard Library: ui/confetti_celebration
# Description: Full-screen particle confetti explosion for achievements
# Author: Star Core Team
# Version: 1.0.0

class ConfettiCelebration
    property name = "confetti_celebration"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: ConfettiCelebration>"
    end
end

function create()
    return ConfettiCelebration()
end

function describe()
    return "Full-screen particle confetti explosion for achievements"
end
