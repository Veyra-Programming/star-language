# Star Standard Library: storage/in_memory_db
# Description: Relational in-memory table with primary keys
# Author: Star Core Team
# Version: 1.0.0

class InMemoryDb
    property name = "in_memory_db"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return InMemoryDb()
end

function describe()
    return "Relational in-memory table with primary keys"
end
