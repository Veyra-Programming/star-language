# Star Standard Library: ui/card_flip_view
# Description: 3D double-sided flipping card with front and back faces
# Author: Star Core Team
# Version: 1.0.0

class CardFlipView
    property name = "card_flip_view"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: CardFlipView>"
    end
end

function create()
    return CardFlipView()
end

function describe()
    return "3D double-sided flipping card with front and back faces"
end
