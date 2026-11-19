# Star Standard Library: ui/box_plot
# Description: Statistical five-number summary box and whisker plot
# Author: Star Core Team
# Version: 1.0.0

class BoxPlot
    property name = "box_plot"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: BoxPlot>"
    end
end

function create()
    return BoxPlot()
end

function describe()
    return "Statistical five-number summary box and whisker plot"
end
