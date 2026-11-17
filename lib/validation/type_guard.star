# Star Standard Library: validation/type_guard
# Description: Runtime type inspection guards
# Author: Star Core Team
# Version: 1.0.0

class TypeGuard
    property name = "type_guard"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return TypeGuard()
end

function describe()
    return "Runtime type inspection guards"
end
