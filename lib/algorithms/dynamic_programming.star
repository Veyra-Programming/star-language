# Star Standard Library: algorithms/dynamic_programming
# Description: DP algorithms for LCS, Fibonacci, and knapsack
# Author: Star Core Team
# Version: 1.0.0

class DynamicProgramming
    property name = "dynamic_programming"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return DynamicProgramming()
end

function describe()
    return "DP algorithms for LCS, Fibonacci, and knapsack"
end
