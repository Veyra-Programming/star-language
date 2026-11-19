# Star Standard Library: ui/back_to_top_button
# Description: Smooth scroll-to-top floating button with progress ring
# Author: Star Core Team
# Version: 1.0.0

class BackToTopButton
    property name = "back_to_top_button"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: BackToTopButton>"
    end
end

function create()
    return BackToTopButton()
end

function describe()
    return "Smooth scroll-to-top floating button with progress ring"
end
