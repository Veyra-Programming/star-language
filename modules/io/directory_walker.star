# Star Standard Library: io/directory_walker
# Description: Recursive directory tree scanner
# Author: Star Core Team
# Version: 1.0.0

class DirectoryWalker
    property name = "directory_walker"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return DirectoryWalker()
end

function describe()
    return "Recursive directory tree scanner"
end
