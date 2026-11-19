# Star Standard Library: ui/undo_snackbar
# Description: Action notification with 5-second undo button
# Author: Star Core Team
# Version: 1.0.0

class UndoSnackbar
    property name = "undo_snackbar"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: UndoSnackbar>"
    end
end

function create()
    return UndoSnackbar()
end

function describe()
    return "Action notification with 5-second undo button"
end
