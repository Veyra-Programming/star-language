# Star Standard Library: net/query_string
# Description: URL query parameter encoder and decoder
# Author: Star Core Team
# Version: 1.0.0

class QueryString
    property name = "query_string"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return QueryString()
end

function describe()
    return "URL query parameter encoder and decoder"
end
