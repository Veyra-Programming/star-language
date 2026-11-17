# Star Standard Library: net/dns
# Description: DNS record types and lookup simulator
# Author: Star Core Team
# Version: 1.0.0

class Dns
    property name = "dns"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return Dns()
end

function describe()
    return "DNS record types and lookup simulator"
end
