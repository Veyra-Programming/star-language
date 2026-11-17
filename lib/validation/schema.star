# Star Standard Library: validation/schema
# Description: Object schema definition and property validation
# Author: Star Core Team
# Version: 1.0.0

class Schema
    property name = "schema"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return Schema()
end

function describe()
    return "Object schema definition and property validation"
end
