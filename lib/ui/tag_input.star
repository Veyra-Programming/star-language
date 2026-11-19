# Star Standard Library: ui/tag_input
# Description: Chip-based tag entry with auto-suggestion and chip removal
# Author: Star Core Team
# Version: 1.0.0

class TagInput
    property name = "tag_input"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: TagInput>"
    end
end

function create()
    return TagInput()
end

function describe()
    return "Chip-based tag entry with auto-suggestion and chip removal"
end
