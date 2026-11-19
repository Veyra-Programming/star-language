# Star Standard Library: ui/two_column_layout
# Description: Standard content plus sidebar layout
# Author: Star Core Team
# Version: 1.0.0

class TwoColumnLayout
    property name = "two_column_layout"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: TwoColumnLayout>"
    end
end

function create()
    return TwoColumnLayout()
end

function describe()
    return "Standard content plus sidebar layout"
end
