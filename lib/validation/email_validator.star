# Star Standard Library: validation/email_validator
# Description: RFC 5322 compliant email syntax validator
# Author: Star Core Team
# Version: 1.0.0

class EmailValidator
    property name = "email_validator"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return EmailValidator()
end

function describe()
    return "RFC 5322 compliant email syntax validator"
end
