# Star Standard Library: ui/rating_bar
# Description: Interactive 5-star or custom icon rating selector
# Author: Star Core Team
# Version: 1.0.0

class RatingBar
    property name = "rating_bar"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: RatingBar>"
    end
end

function create()
    return RatingBar()
end

function describe()
    return "Interactive 5-star or custom icon rating selector"
end
