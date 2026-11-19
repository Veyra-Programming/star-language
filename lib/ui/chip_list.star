# Star Standard Library: ui/chip_list
# Description: Flowing list of interactive chips with delete and select states
# Author: Star Core Team
# Version: 1.0.0

class ChipList
    property name = "chip_list"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: ChipList>"
    end
end

function create()
    return ChipList()
end

function describe()
    return "Flowing list of interactive chips with delete and select states"
end
