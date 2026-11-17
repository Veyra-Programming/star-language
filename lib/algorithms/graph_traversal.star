# Star Standard Library: algorithms/graph_traversal
# Description: Breadth-First Search (BFS) and Depth-First Search (DFS)
# Author: Star Core Team
# Version: 1.0.0

class GraphTraversal
    property name = "graph_traversal"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return GraphTraversal()
end

function describe()
    return "Breadth-First Search (BFS) and Depth-First Search (DFS)"
end
