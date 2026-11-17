# Star Standard Library: algorithms/convex_hull
# Description: 2D Graham Scan convex hull polygon calculation
# Author: Star Core Team
# Version: 1.0.0

class ConvexHull
    property name = "convex_hull"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return ConvexHull()
end

function describe()
    return "2D Graham Scan convex hull polygon calculation"
end
