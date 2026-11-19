# Star Standard Library: ui/multi_select
# Description: Searchable multi-selection dropdown with chip tags
# Author: Star Core Team
# Version: 1.0.0

class MultiSelect
    property name = "multi_select"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: MultiSelect>"
    end
end

function create()
    return MultiSelect()
end

function describe()
    return "Searchable multi-selection dropdown with chip tags"
end
