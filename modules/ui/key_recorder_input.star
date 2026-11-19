# Star Standard Library: ui/key_recorder_input
# Description: Hotkey and keyboard shortcut recorder field
# Author: Star Core Team
# Version: 1.0.0

class KeyRecorderInput
    property name = "key_recorder_input"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: KeyRecorderInput>"
    end
end

function create()
    return KeyRecorderInput()
end

function describe()
    return "Hotkey and keyboard shortcut recorder field"
end
