# Star Standard Library: strings/levenshtein
# Description: String edit distance and similarity ratio
# Author: Star Core Team
# Version: 1.0.0

class Levenshtein
    property name = "levenshtein"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return Levenshtein()
end

function describe()
    return "String edit distance and similarity ratio"
end
