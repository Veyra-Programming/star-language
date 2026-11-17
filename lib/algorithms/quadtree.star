# Star Standard Library: algorithms/quadtree
# Description: 2D spatial partitioning QuadTree
# Author: Star Core Team
# Version: 1.0.0

class Quadtree
    property name = "quadtree"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return Quadtree()
end

function describe()
    return "2D spatial partitioning QuadTree"
end
