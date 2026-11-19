# Star Standard Library: ui/game_hud
# Description: In-game heads-up display with health bar, score, and ammo
# Author: Star Core Team
# Version: 1.0.0

class GameHud
    property name = "game_hud"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: GameHud>"
    end
end

function create()
    return GameHud()
end

function describe()
    return "In-game heads-up display with health bar, score, and ammo"
end
