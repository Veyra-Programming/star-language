# Star Standard Library: collections/graph
# Description: Directed and undirected graph adjacency representation
# Author: Star Core Team
# Version: 1.0.0

class Graph
    property directed = false
    property vertex_count = 0

    function is_directed()
        return self.directed
    end

    function num_vertices()
        return self.vertex_count
    end

end

function create(is_dir)
    return Graph(directed = is_dir, vertex_count = 0)
end
