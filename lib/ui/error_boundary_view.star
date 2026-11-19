# Star Standard Library: ui/error_boundary_view
# Description: Graceful error boundary fallback card with stack trace
# Author: Star Core Team
# Version: 1.0.0

class ErrorBoundaryView
    property name = "error_boundary_view"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: ErrorBoundaryView>"
    end
end

function create()
    return ErrorBoundaryView()
end

function describe()
    return "Graceful error boundary fallback card with stack trace"
end
