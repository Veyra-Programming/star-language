# Star Standard Library: algorithms/topological_sort
# Description: DAG topological sorting with cycle detection
# Author: Star Core Team
# Version: 1.0.0

class TopologicalSort
    property name = "topological_sort"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return TopologicalSort()
end

function describe()
    return "DAG topological sorting with cycle detection"
end
