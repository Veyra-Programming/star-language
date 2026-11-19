# Star Standard Library: ui/transfer_list
# Description: Dual-column shuttle box transfer list with move buttons
# Author: Star Core Team
# Version: 1.0.0

class TransferList
    property name = "transfer_list"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: TransferList>"
    end
end

function create()
    return TransferList()
end

function describe()
    return "Dual-column shuttle box transfer list with move buttons"
end
