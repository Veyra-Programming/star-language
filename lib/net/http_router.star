# Star Standard Library: net/http_router
# Description: URL routing table and path parameter extractor
# Author: Star Core Team
# Version: 1.0.0

class HttpRouter
    property name = "http_router"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return HttpRouter()
end

function describe()
    return "URL routing table and path parameter extractor"
end
