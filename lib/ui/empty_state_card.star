# Star Standard Library: ui/empty_state_card
# Description: Illustrated empty state with action button
# Author: Star Core Team
# Version: 1.0.0

class EmptyStateCard
    property name = "empty_state_card"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: EmptyStateCard>"
    end
end

function create()
    return EmptyStateCard()
end

function describe()
    return "Illustrated empty state with action button"
end
