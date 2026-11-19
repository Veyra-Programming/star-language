# Star Standard Library: ui/accordion_table
# Description: Data table where rows expand into detailed nested views
# Author: Star Core Team
# Version: 1.0.0

class AccordionTable
    property name = "accordion_table"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: AccordionTable>"
    end
end

function create()
    return AccordionTable()
end

function describe()
    return "Data table where rows expand into detailed nested views"
end
