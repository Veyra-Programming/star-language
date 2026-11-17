# Star Standard Library: ui/dialog_builder
# Description: Modal dialog specification and action buttons
# Author: Star Core Team
# Version: 1.0.0

class DialogBuilder
    property name = "dialog_builder"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return DialogBuilder()
end

function describe()
    return "Modal dialog specification and action buttons"
end
