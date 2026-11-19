# Star Standard Library: ui/avatar_editor
# Description: Circular avatar upload, reposition, and zoom editor
# Author: Star Core Team
# Version: 1.0.0

class AvatarEditor
    property name = "avatar_editor"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: AvatarEditor>"
    end
end

function create()
    return AvatarEditor()
end

function describe()
    return "Circular avatar upload, reposition, and zoom editor"
end
