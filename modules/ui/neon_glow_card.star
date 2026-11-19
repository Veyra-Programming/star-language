# Star Standard Library: ui/neon_glow_card
# Description: Glowing neon cyberpunk card with border animations
# Author: Star Core Team
# Version: 1.0.0

class NeonGlowCard
    property name = "neon_glow_card"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: NeonGlowCard>"
    end
end

function create()
    return NeonGlowCard()
end

function describe()
    return "Glowing neon cyberpunk card with border animations"
end
