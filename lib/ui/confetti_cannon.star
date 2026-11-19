# Star Standard Library: ui/confetti_cannon
# Description: Celebratory confetti particle burst physics emitter
# Author: Star Core Team
# Version: 1.0.0

class ConfettiCannon
    property name = "confetti_cannon"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: ConfettiCannon>"
    end
end

function create()
    return ConfettiCannon()
end

function describe()
    return "Celebratory confetti particle burst physics emitter"
end
