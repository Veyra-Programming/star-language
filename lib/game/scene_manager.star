# Star Standard Library: game/scene_manager
# Description: Game scene stack and stage transition manager
# Author: Star Core Team
# Version: 1.0.0

class SceneManager
    property name = "scene_manager"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return SceneManager()
end

function describe()
    return "Game scene stack and stage transition manager"
end
