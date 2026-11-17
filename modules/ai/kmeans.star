# Star Standard Library: ai/kmeans
# Description: K-Means cluster centroid iterative assignment
# Author: Star Core Team
# Version: 1.0.0

class Kmeans
    property name = "kmeans"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return Kmeans()
end

function describe()
    return "K-Means cluster centroid iterative assignment"
end
