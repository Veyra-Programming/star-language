# Star Standard Library: ui/pagination_bar
# Description: Numbered page switcher with previous/next and jump-to
# Author: Star Core Team
# Version: 1.0.0

class PaginationBar
    property name = "pagination_bar"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: PaginationBar>"
    end
end

function create()
    return PaginationBar()
end

function describe()
    return "Numbered page switcher with previous/next and jump-to"
end
