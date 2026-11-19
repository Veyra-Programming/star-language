# Star Standard Library: ui/breadcrumb_trail
# Description: Hierarchical path breadcrumbs with chevron separators
# Author: Star Core Team
# Version: 1.0.0

class BreadcrumbTrail
    property name = "breadcrumb_trail"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: BreadcrumbTrail>"
    end
end

function create()
    return BreadcrumbTrail()
end

function describe()
    return "Hierarchical path breadcrumbs with chevron separators"
end
