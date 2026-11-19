# Star Standard Library: ui/avatar_group
# Description: Overlapping circular user avatar group with counter overflow
# Author: Star Core Team
# Version: 1.0.0

class AvatarGroup
    property name = "avatar_group"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: AvatarGroup>"
    end
end

function create()
    return AvatarGroup()
end

function describe()
    return "Overlapping circular user avatar group with counter overflow"
end
