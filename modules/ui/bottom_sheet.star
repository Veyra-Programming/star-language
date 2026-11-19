# Star Standard Library: ui/bottom_sheet
# Description: Swipeable mobile bottom modal sheet with grab handle
# Author: Star Core Team
# Version: 1.0.0

class BottomSheet
    property name = "bottom_sheet"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: BottomSheet>"
    end
end

function create()
    return BottomSheet()
end

function describe()
    return "Swipeable mobile bottom modal sheet with grab handle"
end
