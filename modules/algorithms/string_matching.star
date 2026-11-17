# Star Standard Library: algorithms/string_matching
# Description: KMP and Rabin-Karp substring search algorithms
# Author: Star Core Team
# Version: 1.0.0

class StringMatching
    property name = "string_matching"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return StringMatching()
end

function describe()
    return "KMP and Rabin-Karp substring search algorithms"
end
