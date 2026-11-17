# Star Standard Library: sys/benchmark
# Description: Micro-benchmark timer and operations-per-second
# Author: Star Core Team
# Version: 1.0.0

class Benchmark
    property name = "benchmark"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return Benchmark()
end

function describe()
    return "Micro-benchmark timer and operations-per-second"
end
