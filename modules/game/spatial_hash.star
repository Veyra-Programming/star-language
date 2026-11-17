# Star Standard Library: game/spatial_hash
# Description: Spatial hashing for broadphase collision detection
# Author: Star Core Team
# Version: 1.0.0

class SpatialHash
    property name = "spatial_hash"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return SpatialHash()
end

function describe()
    return "Spatial hashing for broadphase collision detection"
end
