# Star Standard Library: ui/hint_pointer
# Description: Animated pulsating arrow pointer highlighting new features
# Author: Star Core Team
# Version: 1.0.0

class HintPointer
    property name = "hint_pointer"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: HintPointer>"
    end
end

function create()
    return HintPointer()
end

function describe()
    return "Animated pulsating arrow pointer highlighting new features"
end
