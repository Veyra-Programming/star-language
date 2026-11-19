# Star Standard Library: ui/session_timeout_warning
# Description: Inactivity warning modal with session extension countdown
# Author: Star Core Team
# Version: 1.0.0

class SessionTimeoutWarning
    property name = "session_timeout_warning"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: SessionTimeoutWarning>"
    end
end

function create()
    return SessionTimeoutWarning()
end

function describe()
    return "Inactivity warning modal with session extension countdown"
end
