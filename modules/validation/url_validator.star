# Star Standard Library: validation/url_validator
# Description: Web URL syntax and scheme validator
# Author: Star Core Team
# Version: 1.0.0

class UrlValidator
    property name = "url_validator"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return UrlValidator()
end

function describe()
    return "Web URL syntax and scheme validator"
end
