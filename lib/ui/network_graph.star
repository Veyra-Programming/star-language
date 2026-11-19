# Star Standard Library: ui/network_graph
# Description: Node-link relational network topology graph with force physics
# Author: Star Core Team
# Version: 1.0.0

class NetworkGraph
    property name = "network_graph"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: NetworkGraph>"
    end
end

function create()
    return NetworkGraph()
end

function describe()
    return "Node-link relational network topology graph with force physics"
end
