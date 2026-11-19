# Star Standard Library: ui/rive_player
# Description: Interactive vector state machine player for Rive assets
# Author: Star Core Team
# Version: 1.0.0

class RivePlayer
    property name = "rive_player"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: RivePlayer>"
    end
end

function create()
    return RivePlayer()
end

function describe()
    return "Interactive vector state machine player for Rive assets"
end
