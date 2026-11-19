# Star Standard Library: ui/modal_dialog
# Description: Centered pop-up modal dialog with backdrop blur and escape key
# Author: Star Core Team
# Version: 1.0.0

class ModalDialog
    property name = "modal_dialog"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: ModalDialog>"
    end
end

function create()
    return ModalDialog()
end

function describe()
    return "Centered pop-up modal dialog with backdrop blur and escape key"
end
