# Star Standard Library: mobile/network_info
# Description: Cellular and WiFi connection state query
# Author: Star Core Team
# Version: 1.0.0

class NetworkInfo
    property name = "network_info"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return NetworkInfo()
end

function describe()
    return "Cellular and WiFi connection state query"
end
