# Star Standard Library: strings/regex_lite
# Description: Pattern matching and wildcard validation helpers
# Author: Star Core Team
# Version: 1.0.0

class RegexLite
    property name = "regex_lite"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return RegexLite()
end

function describe()
    return "Pattern matching and wildcard validation helpers"
end
