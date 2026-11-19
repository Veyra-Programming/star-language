# Star Standard Library: ui/slot_machine_spinner
# Description: Casino-style slot machine spinning reel component
# Author: Star Core Team
# Version: 1.0.0

class SlotMachineSpinner
    property name = "slot_machine_spinner"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: SlotMachineSpinner>"
    end
end

function create()
    return SlotMachineSpinner()
end

function describe()
    return "Casino-style slot machine spinning reel component"
end
