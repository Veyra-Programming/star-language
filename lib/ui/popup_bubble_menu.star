# Star Standard Library: ui/popup_bubble_menu
# Description: Pointing bubble menu positioned relative to trigger element
# Author: Star Core Team
# Version: 1.0.0

class PopupBubbleMenu
    property name = "popup_bubble_menu"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: PopupBubbleMenu>"
    end
end

function create()
    return PopupBubbleMenu()
end

function describe()
    return "Pointing bubble menu positioned relative to trigger element"
end
