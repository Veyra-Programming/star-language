# Star Standard Library: test/test_suite
# Description: Test suite group manager
# Author: Star Core Team
# Version: 1.0.0

class TestSuite
    property name = "test_suite"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return TestSuite()
end

function describe()
    return "Test suite group manager"
end
