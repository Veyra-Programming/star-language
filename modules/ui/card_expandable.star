# Star Standard Library: ui/card_expandable
# Description: Card that smoothly animates and unfolds to reveal details
# Author: Star Core Team
# Version: 1.0.0

class CardExpandable
    property name = "card_expandable"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: CardExpandable>"
    end
end

function create()
    return CardExpandable()
end

function describe()
    return "Card that smoothly animates and unfolds to reveal details"
end
