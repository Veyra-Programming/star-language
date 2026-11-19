# Star Standard Library: ui/network_offline_banner
# Description: Red sticky banner warning when internet drops
# Author: Star Core Team
# Version: 1.0.0

class NetworkOfflineBanner
    property name = "network_offline_banner"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: NetworkOfflineBanner>"
    end
end

function create()
    return NetworkOfflineBanner()
end

function describe()
    return "Red sticky banner warning when internet drops"
end
