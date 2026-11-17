# Star Standard Library: io/file_utils
# Description: File system read, write, append, and existence tests
# Author: Star Core Team
# Version: 1.0.0

class FileUtils
    property name = "file_utils"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return FileUtils()
end

function describe()
    return "File system read, write, append, and existence tests"
end
