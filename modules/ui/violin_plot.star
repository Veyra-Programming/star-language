# Star Standard Library: ui/violin_plot
# Description: Statistical kernel density violin plot with quartiles
# Author: Star Core Team
# Version: 1.0.0

class ViolinPlot
    property name = "violin_plot"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: ViolinPlot>"
    end
end

function create()
    return ViolinPlot()
end

function describe()
    return "Statistical kernel density violin plot with quartiles"
end
