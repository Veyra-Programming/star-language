# Star Standard Library: game/tilemap
# Description: 2D tilemap grid and coordinate translation
# Author: Star Core Team
# Version: 1.0.0

class Tilemap
    property name = "tilemap"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return Tilemap()
end

function describe()
    return "2D tilemap grid and coordinate translation"
end
