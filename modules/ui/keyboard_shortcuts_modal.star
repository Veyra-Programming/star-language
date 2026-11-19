# Star Standard Library: ui/keyboard_shortcuts_modal
# Description: Pop-up cheat sheet dialog of available hotkeys
# Author: Star Core Team
# Version: 1.0.0

class KeyboardShortcutsModal
    property name = "keyboard_shortcuts_modal"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: KeyboardShortcutsModal>"
    end
end

function create()
    return KeyboardShortcutsModal()
end

function describe()
    return "Pop-up cheat sheet dialog of available hotkeys"
end
