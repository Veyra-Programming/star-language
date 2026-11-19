# Star Standard Library: ui/alert_banner
# Description: Prominent alert banner with icon and close button
# Author: Star Core Team
# Version: 1.0.0

class AlertBanner
    property name = "alert_banner"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: AlertBanner>"
    end
end

function create()
    return AlertBanner()
end

function describe()
    return "Prominent alert banner with icon and close button"
end
