# Star Standard Library: test/snapshot
# Description: Snapshot testing serializer and comparator
# Author: Star Core Team
# Version: 1.0.0

class Snapshot
    property name = "snapshot"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return Snapshot()
end

function describe()
    return "Snapshot testing serializer and comparator"
end
