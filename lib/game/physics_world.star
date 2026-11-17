# Star Standard Library: game/physics_world
# Description: 2D physics simulator with gravity and damping
# Author: Star Core Team
# Version: 1.0.0

class PhysicsWorld
    property name = "physics_world"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return PhysicsWorld()
end

function describe()
    return "2D physics simulator with gravity and damping"
end
