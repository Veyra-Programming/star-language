# Star Standard Library: algorithms/pathfinding
# Description: A* search and Dijkstra shortest path finding
# Author: Star Core Team
# Version: 1.0.0

class Pathfinding
    property name = "pathfinding"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return Pathfinding()
end

function describe()
    return "A* search and Dijkstra shortest path finding"
end
