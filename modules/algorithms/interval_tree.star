# Star Standard Library: algorithms/interval_tree
# Description: 1D interval overlap detection queries
# Author: Star Core Team
# Version: 1.0.0

class IntervalTree
    property name = "interval_tree"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return IntervalTree()
end

function describe()
    return "1D interval overlap detection queries"
end
