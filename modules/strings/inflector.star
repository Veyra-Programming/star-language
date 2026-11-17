# Star Standard Library: strings/inflector
# Description: Noun pluralization, singularization, and titleizing
# Author: Star Core Team
# Version: 1.0.0

class Inflector
    property name = "inflector"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return Inflector()
end

function describe()
    return "Noun pluralization, singularization, and titleizing"
end
