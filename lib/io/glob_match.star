# Star Standard Library: io/glob_match
# Description: Wildcard glob pattern matching for file searches
# Author: Star Core Team
# Version: 1.0.0

class GlobMatch
    property name = "glob_match"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return GlobMatch()
end

function describe()
    return "Wildcard glob pattern matching for file searches"
end
