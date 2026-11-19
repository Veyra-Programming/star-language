# Star Standard Library: ui/rate_app_dialog
# Description: Star rating prompt dialog asking for user feedback
# Author: Star Core Team
# Version: 1.0.0

class RateAppDialog
    property name = "rate_app_dialog"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: RateAppDialog>"
    end
end

function create()
    return RateAppDialog()
end

function describe()
    return "Star rating prompt dialog asking for user feedback"
end
