# Star Standard Library: io/temp_file
# Description: Temporary file naming and directory sandbox
# Author: Star Core Team
# Version: 1.0.0

class TempFile
    property name = "temp_file"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return TempFile()
end

function describe()
    return "Temporary file naming and directory sandbox"
end
