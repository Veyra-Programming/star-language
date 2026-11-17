# Star Standard Library: math/stats
# Description: Statistical summaries including mean, variance, and standard deviation
# Author: Star Core Team
# Version: 1.0.0

class StatsSummary
    property count = 0
    property sum = 0.0
    property mean = 0.0

    function summary()
        return "Count: " + self.count + ", Mean: " + self.mean
    end

end

function mean(values)
    if len(values) == 0
    return 0.0
    end
    variable total = 0.0
    for v in values
    total = total + v
    end
    return total / len(values)
end

function min_value(values)
    if len(values) == 0
    return 0
    end
    variable m = values[0]
    for v in values
    if v < m
    m = v
    end
    end
    return m
end

function max_value(values)
    if len(values) == 0
    return 0
    end
    variable m = values[0]
    for v in values
    if v > m
    m = v
    end
    end
    return m
end
