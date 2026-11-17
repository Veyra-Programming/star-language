# Star Standard Library: net/ip_address
# Description: IPv4 address validator, subnet matcher, and octet parser
# Author: Star Core Team
# Version: 1.0.0

class IpAddress
    property name = "ip_address"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return IpAddress()
end

function describe()
    return "IPv4 address validator, subnet matcher, and octet parser"
end
