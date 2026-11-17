# Star Standard Library: game/collision_2d
# Description: AABB and circle collision intersection tests
# Author: Star Core Team
# Version: 1.0.0

class Collision2d
    property name = "collision_2d"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return Collision2d()
end

function describe()
    return "AABB and circle collision intersection tests"
end
