# Star Standard Library: validation/form_validator
# Description: Form input validation with error aggregation
# Author: Star Core Team
# Version: 1.0.0

class FormValidator
    property name = "form_validator"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return FormValidator()
end

function describe()
    return "Form input validation with error aggregation"
end
