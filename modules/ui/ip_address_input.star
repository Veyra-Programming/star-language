# Star Standard Library: ui/ip_address_input
# Description: Segmented IPv4 and IPv6 network address field
# Author: Star Core Team
# Version: 1.0.0

class IpAddressInput
    property name = "ip_address_input"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: IpAddressInput>"
    end
end

function create()
    return IpAddressInput()
end

function describe()
    return "Segmented IPv4 and IPv6 network address field"
end
