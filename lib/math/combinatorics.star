# Star Standard Library: math/combinatorics
# Description: Combinatorial arithmetic including factorials, permutations, and combinations
# Author: Star Core Team
# Version: 1.0.0

class PermutationCounter
    property base = 1

    function get_base()
        return self.base
    end

end

function factorial(n)
    if n <= 1
    return 1
    end
    variable res = 1
    variable i = 2
    while i <= n
    res = res * i
    i = i + 1
    end
    return res
end

function permutations(n, r)
    return factorial(n) / factorial(n - r)
end

function combinations(n, r)
    return factorial(n) / (factorial(r) * factorial(n - r))
end
