# Star Standard Library: test/fixture
# Description: Test setup and teardown lifecycle context
# Author: Star Core Team
# Version: 1.0.0

class Fixture
    property name = "fixture"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return Fixture()
end

function describe()
    return "Test setup and teardown lifecycle context"
end
