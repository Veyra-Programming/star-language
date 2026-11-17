# Star Standard Library: test/benchmark_runner
# Description: Benchmark test runner with warmup passes
# Author: Star Core Team
# Version: 1.0.0

class BenchmarkRunner
    property name = "benchmark_runner"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return BenchmarkRunner()
end

function describe()
    return "Benchmark test runner with warmup passes"
end
