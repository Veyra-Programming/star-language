# Star Standard Library: test/coverage_lite
# Description: Statement coverage tracker
# Author: Star Core Team
# Version: 1.0.0

class CoverageLite
    property name = "coverage_lite"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return CoverageLite()
end

function describe()
    return "Statement coverage tracker"
end
