# Star Standard Library: ui/progress_bar
# Description: Linear animated progress bar with gradient and striped styles
# Author: Star Core Team
# Version: 1.0.0

class ProgressBar
    property name = "progress_bar"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: ProgressBar>"
    end
end

function create()
    return ProgressBar()
end

function describe()
    return "Linear animated progress bar with gradient and striped styles"
end
