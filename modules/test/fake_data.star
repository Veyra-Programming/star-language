# Star Standard Library: test/fake_data
# Description: Mock dataset generator for names, emails, and numbers
# Author: Star Core Team
# Version: 1.0.0

class FakeData
    property name = "fake_data"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return FakeData()
end

function describe()
    return "Mock dataset generator for names, emails, and numbers"
end
