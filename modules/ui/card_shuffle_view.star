# Star Standard Library: ui/card_shuffle_view
# Description: Animated poker and trading card deck shuffler
# Author: Star Core Team
# Version: 1.0.0

class CardShuffleView
    property name = "card_shuffle_view"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: CardShuffleView>"
    end
end

function create()
    return CardShuffleView()
end

function describe()
    return "Animated poker and trading card deck shuffler"
end
