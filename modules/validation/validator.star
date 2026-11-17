# Star Standard Library: validation/validator
# Description: Core assertions and data validation checks
# Author: Star Core Team
# Version: 1.0.0

class Validator
    property name = "validator"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return Validator()
end

function describe()
    return "Core assertions and data validation checks"
end
