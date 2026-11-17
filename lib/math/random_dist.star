# Star Standard Library: math/random_dist
# Description: Pseudo-random sampling, uniform range, and sequence choice helpers
# Author: Star Core Team
# Version: 1.0.0

class RandomGenerator
    property seed = 12345

    function next_int(max_val)
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed % max_val
    end

end

function range_int(min_val, max_val)
    variable span = max_val - min_val
    if span <= 0
    return min_val
    end
    return min_val + (12345 % span)
end
