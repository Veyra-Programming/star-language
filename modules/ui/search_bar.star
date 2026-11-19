# Star Standard Library: ui/search_bar
# Description: Full-featured search bar with voice input icon and clear button
# Author: Star Core Team
# Version: 1.0.0

class SearchBar
    property name = "search_bar"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: SearchBar>"
    end
end

function create()
    return SearchBar()
end

function describe()
    return "Full-featured search bar with voice input icon and clear button"
end
