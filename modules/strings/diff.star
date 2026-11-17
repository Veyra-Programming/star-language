# Star Standard Library: strings/diff
# Description: Line-by-line and character diff utilities
# Author: Star Core Team
# Version: 1.0.0

class Diff
    property name = "diff"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return Diff()
end

function describe()
    return "Line-by-line and character diff utilities"
end
