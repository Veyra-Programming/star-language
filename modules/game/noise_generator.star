# Star Standard Library: game/noise_generator
# Description: Perlin and Simplex gradient noise generator
# Author: Star Core Team
# Version: 1.0.0

class NoiseGenerator
    property name = "noise_generator"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return NoiseGenerator()
end

function describe()
    return "Perlin and Simplex gradient noise generator"
end
