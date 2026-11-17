# Star Standard Library: algorithms/clustering_lite
# Description: Centroid distance and 2D cluster assignment
# Author: Star Core Team
# Version: 1.0.0

class ClusteringLite
    property name = "clustering_lite"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return ClusteringLite()
end

function describe()
    return "Centroid distance and 2D cluster assignment"
end
