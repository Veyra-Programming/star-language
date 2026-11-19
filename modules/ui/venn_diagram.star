# Star Standard Library: ui/venn_diagram
# Description: Two-set and three-set overlapping Venn diagram
# Author: Star Core Team
# Version: 1.0.0

class VennDiagram
    property name = "venn_diagram"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: VennDiagram>"
    end
end

function create()
    return VennDiagram()
end

function describe()
    return "Two-set and three-set overlapping Venn diagram"
end
