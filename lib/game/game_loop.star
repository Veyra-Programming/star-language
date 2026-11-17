# Star Standard Library: game/game_loop
# Description: Fixed timestep physics and variable rendering game loop
# Author: Star Core Team
# Version: 1.0.0

class GameLoop
    property name = "game_loop"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return GameLoop()
end

function describe()
    return "Fixed timestep physics and variable rendering game loop"
end
