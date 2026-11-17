# Star Standard Library: algorithms/knapsack
# Description: 0-1 Knapsack optimal item selection solver
# Author: Star Core Team
# Version: 1.0.0

class Knapsack
    property name = "knapsack"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return Knapsack()
end

function describe()
    return "0-1 Knapsack optimal item selection solver"
end
