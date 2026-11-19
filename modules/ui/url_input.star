# Star Standard Library: ui/url_input
# Description: Validated web URL input with protocol prefix pill
# Author: Star Core Team
# Version: 1.0.0

class UrlInput
    property name = "url_input"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: UrlInput>"
    end
end

function create()
    return UrlInput()
end

function describe()
    return "Validated web URL input with protocol prefix pill"
end
