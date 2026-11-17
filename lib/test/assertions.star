# Star Standard Library: test/assertions
# Description: Unit testing assertions (equal, true, false, null)
# Author: Star Core Team
# Version: 1.0.0

class Assertions
    property name = "assertions"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return Assertions()
end

function describe()
    return "Unit testing assertions (equal, true, false, null)"
end
