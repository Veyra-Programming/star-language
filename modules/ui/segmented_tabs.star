# Star Standard Library: ui/segmented_tabs
# Description: Pill-shaped segmented tabs for dashboard views
# Author: Star Core Team
# Version: 1.0.0

class SegmentedTabs
    property name = "segmented_tabs"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: SegmentedTabs>"
    end
end

function create()
    return SegmentedTabs()
end

function describe()
    return "Pill-shaped segmented tabs for dashboard views"
end
