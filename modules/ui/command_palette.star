# Star Standard Library: ui/command_palette
# Description: Keyboard-driven Cmd+K / Ctrl+K search and action launcher
# Author: Star Core Team
# Version: 1.0.0

class CommandPalette
    property name = "command_palette"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: CommandPalette>"
    end
end

function create()
    return CommandPalette()
end

function describe()
    return "Keyboard-driven Cmd+K / Ctrl+K search and action launcher"
end
