# Star Standard Library: ui/loading_spinner
# Description: Modern rotating ring and dual-ring loading spinner
# Author: Star Core Team
# Version: 1.0.0

class LoadingSpinner
    property name = "loading_spinner"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: LoadingSpinner>"
    end
end

function create()
    return LoadingSpinner()
end

function describe()
    return "Modern rotating ring and dual-ring loading spinner"
end
