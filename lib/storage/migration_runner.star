# Star Standard Library: storage/migration_runner
# Description: Database schema migration version tracker
# Author: Star Core Team
# Version: 1.0.0

class MigrationRunner
    property name = "migration_runner"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return MigrationRunner()
end

function describe()
    return "Database schema migration version tracker"
end
