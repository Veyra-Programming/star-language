# Star Standard Library: ui/hamburger_button
# Description: Animated morphing hamburger-to-close icon button
# Author: Star Core Team
# Version: 1.0.0

class HamburgerButton
    property name = "hamburger_button"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: HamburgerButton>"
    end
end

function create()
    return HamburgerButton()
end

function describe()
    return "Animated morphing hamburger-to-close icon button"
end
