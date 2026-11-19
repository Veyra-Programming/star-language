# Star Standard Library: ui/key_value_table
# Description: Clean two-column property-value inspector table
# Author: Star Core Team
# Version: 1.0.0

class KeyValueTable
    property name = "key_value_table"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: KeyValueTable>"
    end
end

function create()
    return KeyValueTable()
end

function describe()
    return "Clean two-column property-value inspector table"
end
