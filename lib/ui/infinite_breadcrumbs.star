# Star Standard Library: ui/infinite_breadcrumbs
# Description: Auto-collapsing long breadcrumb path with ellipsis menu
# Author: Star Core Team
# Version: 1.0.0

class InfiniteBreadcrumbs
    property name = "infinite_breadcrumbs"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: InfiniteBreadcrumbs>"
    end
end

function create()
    return InfiniteBreadcrumbs()
end

function describe()
    return "Auto-collapsing long breadcrumb path with ellipsis menu"
end
