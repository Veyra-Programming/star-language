# Star Standard Library: ui/walkthrough_tour
# Description: Multi-step interactive feature tour overlay with spotlights
# Author: Star Core Team
# Version: 1.0.0

class WalkthroughTour
    property name = "walkthrough_tour"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: WalkthroughTour>"
    end
end

function create()
    return WalkthroughTour()
end

function describe()
    return "Multi-step interactive feature tour overlay with spotlights"
end
