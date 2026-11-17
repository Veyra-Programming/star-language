# Star Standard Library: formats/tar_lite
# Description: TAR archive 512-byte block and header builder
# Author: Star Core Team
# Version: 1.0.0

class TarLite
    property name = "tar_lite"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return TarLite()
end

function describe()
    return "TAR archive 512-byte block and header builder"
end
