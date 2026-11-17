# Star Standard Library: net/http_client
# Description: HTTP client helpers, status codes, and request options
# Author: Star Core Team
# Version: 1.0.0

class HttpClient
    property name = "http_client"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return HttpClient()
end

function describe()
    return "HTTP client helpers, status codes, and request options"
end
