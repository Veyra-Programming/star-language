# Star Standard Library: test/spy
# Description: Spy wrapper monitoring function invocation
# Author: Star Core Team
# Version: 1.0.0

class Spy
    property name = "spy"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return Spy()
end

function describe()
    return "Spy wrapper monitoring function invocation"
end
