# Star Standard Library: storage/json_db
# Description: JSON document database with query matching
# Author: Star Core Team
# Version: 1.0.0

class JsonDb
    property name = "json_db"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return JsonDb()
end

function describe()
    return "JSON document database with query matching"
end
