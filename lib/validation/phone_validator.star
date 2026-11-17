# Star Standard Library: validation/phone_validator
# Description: International E.164 phone number checker
# Author: Star Core Team
# Version: 1.0.0

class PhoneValidator
    property name = "phone_validator"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return PhoneValidator()
end

function describe()
    return "International E.164 phone number checker"
end
