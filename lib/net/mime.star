# Star Standard Library: net/mime
# Description: MIME content-type mappings for web assets
# Author: Star Core Team
# Version: 1.0.0

class Mime
    property name = "mime"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return Mime()
end

function describe()
    return "MIME content-type mappings for web assets"
end
