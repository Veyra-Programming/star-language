# Star Standard Library: ui/card_layout
# Description: Card component container with header, body, actions
# Author: Star Core Team
# Version: 1.0.0

class CardLayout
    property name = "card_layout"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return CardLayout()
end

function describe()
    return "Card component container with header, body, actions"
end
