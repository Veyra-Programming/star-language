# Star Standard Library: net/url
# Description: URL parser for schemes, hosts, ports, paths, and queries
# Author: Star Core Team
# Version: 1.0.0

class Url
    property name = "url"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return Url()
end

function describe()
    return "URL parser for schemes, hosts, ports, paths, and queries"
end
