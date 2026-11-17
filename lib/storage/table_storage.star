# Star Standard Library: storage/table_storage
# Description: Tabular schema with row insertion and filtering
# Author: Star Core Team
# Version: 1.0.0

class TableStorage
    property name = "table_storage"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return TableStorage()
end

function describe()
    return "Tabular schema with row insertion and filtering"
end
