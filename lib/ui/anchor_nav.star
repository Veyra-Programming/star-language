# Star Standard Library: ui/anchor_nav
# Description: Sticky on-page table-of-contents anchor scroll navigation
# Author: Star Core Team
# Version: 1.0.0

class AnchorNav
    property name = "anchor_nav"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: AnchorNav>"
    end
end

function create()
    return AnchorNav()
end

function describe()
    return "Sticky on-page table-of-contents anchor scroll navigation"
end
