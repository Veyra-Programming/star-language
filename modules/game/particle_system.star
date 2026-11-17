# Star Standard Library: game/particle_system
# Description: Particle emitter with velocity, gravity, and lifespan
# Author: Star Core Team
# Version: 1.0.0

class ParticleSystem
    property name = "particle_system"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return ParticleSystem()
end

function describe()
    return "Particle emitter with velocity, gravity, and lifespan"
end
