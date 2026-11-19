# Star Standard Library: ui/progress_dialog
# Description: Modal progress dialog for long-running operations
# Author: Star Core Team
# Version: 1.0.0

class ProgressDialog
    property name = "progress_dialog"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: ProgressDialog>"
    end
end

function create()
    return ProgressDialog()
end

function describe()
    return "Modal progress dialog for long-running operations"
end
