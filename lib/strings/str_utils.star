# Star Standard Library: strings/str_utils
# Description: String manipulation helpers, padding, casing, and trimming
# Author: Star Core Team
# Version: 1.0.0

class StrUtils
    property name = "str_utils"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return StrUtils()
end

function describe()
    return "String manipulation helpers, padding, casing, and trimming"
end
