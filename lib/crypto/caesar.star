# Star Standard Library: crypto/caesar
# Description: Caesar substitution cipher with customizable shift
# Author: Star Core Team
# Version: 1.0.0

class Caesar
    property name = "caesar"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return Caesar()
end

function describe()
    return "Caesar substitution cipher with customizable shift"
end
