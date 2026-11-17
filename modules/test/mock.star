# Star Standard Library: test/mock
# Description: Function mock with call counter and argument logging
# Author: Star Core Team
# Version: 1.0.0

class Mock
    property name = "mock"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return Mock()
end

function describe()
    return "Function mock with call counter and argument logging"
end
