# Star Standard Library: ui/quick_links_bar
# Description: Compact quick-access toolbar for tools and shortcuts
# Author: Star Core Team
# Version: 1.0.0

class QuickLinksBar
    property name = "quick_links_bar"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: QuickLinksBar>"
    end
end

function create()
    return QuickLinksBar()
end

function describe()
    return "Compact quick-access toolbar for tools and shortcuts"
end
