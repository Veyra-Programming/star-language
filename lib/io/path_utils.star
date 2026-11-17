# Star Standard Library: io/path_utils
# Description: File path normalization, extension, and dirname logic
# Author: Star Core Team
# Version: 1.0.0

class PathUtils
    property name = "path_utils"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return PathUtils()
end

function describe()
    return "File path normalization, extension, and dirname logic"
end
