# Star Standard Library: ui/confirm_dialog
# Description: Destructive action confirmation dialog with confirm/cancel
# Author: Star Core Team
# Version: 1.0.0

class ConfirmDialog
    property name = "confirm_dialog"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: ConfirmDialog>"
    end
end

function create()
    return ConfirmDialog()
end

function describe()
    return "Destructive action confirmation dialog with confirm/cancel"
end
