# Star Standard Library: ui/empty_state_view
# Description: Illustrated empty state with call-to-action button
# Author: Star Core Team
# Version: 1.0.0

class EmptyStateView
    property name = "empty_state_view"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: EmptyStateView>"
    end
end

function create()
    return EmptyStateView()
end

function describe()
    return "Illustrated empty state with call-to-action button"
end
