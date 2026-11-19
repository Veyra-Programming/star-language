# Star Standard Library: ui/snackbar
# Description: Material bottom snackbar notice with action button
# Author: Star Core Team
# Version: 1.0.0

class Snackbar
    property name = "snackbar"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: Snackbar>"
    end
end

function create()
    return Snackbar()
end

function describe()
    return "Material bottom snackbar notice with action button"
end
