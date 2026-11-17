# Star Standard Library: test/test_runner
# Description: Test suite collector, execution harness, and reporter
# Author: Star Core Team
# Version: 1.0.0

class TestRunner
    property name = "test_runner"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return TestRunner()
end

function describe()
    return "Test suite collector, execution harness, and reporter"
end
