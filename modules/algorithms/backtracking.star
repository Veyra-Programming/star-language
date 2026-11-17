# Star Standard Library: algorithms/backtracking
# Description: Backtracking search template and constraint solver
# Author: Star Core Team
# Version: 1.0.0

class Backtracking
    property name = "backtracking"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return Backtracking()
end

function describe()
    return "Backtracking search template and constraint solver"
end
