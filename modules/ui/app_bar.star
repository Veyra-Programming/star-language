# Star Standard Library: ui/app_bar
# Description: Top application bar with navigation icon, title, and action buttons
# Author: Star Core Team
# Version: 1.0.0

class AppBar
    property name = "app_bar"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: AppBar>"
    end
end

function create()
    return AppBar()
end

function describe()
    return "Top application bar with navigation icon, title, and action buttons"
end
