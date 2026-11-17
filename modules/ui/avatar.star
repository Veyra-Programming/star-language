# Star Standard Library: ui/avatar
# Description: User profile picture and monogram avatar generator
# Author: Star Core Team
# Version: 1.0.0

class Avatar
    property name = "avatar"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return Avatar()
end

function describe()
    return "User profile picture and monogram avatar generator"
end
