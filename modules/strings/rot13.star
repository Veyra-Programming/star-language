# Star Standard Library: strings/rot13
# Description: ROT13 and Caesar cipher text transformations
# Author: Star Core Team
# Version: 1.0.0

class Rot13
    property name = "rot13"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return Rot13()
end

function describe()
    return "ROT13 and Caesar cipher text transformations"
end
