# Star Standard Library: storage/query_builder
# Description: SQL-like SELECT, WHERE, ORDER BY query builder
# Author: Star Core Team
# Version: 1.0.0

class QueryBuilder
    property name = "query_builder"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return QueryBuilder()
end

function describe()
    return "SQL-like SELECT, WHERE, ORDER BY query builder"
end
