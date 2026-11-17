# Star Standard Library: formats/zip_lite
# Description: ZIP file directory entry and header creator
# Author: Star Core Team
# Version: 1.0.0

class ZipLite
    property name = "zip_lite"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return ZipLite()
end

function describe()
    return "ZIP file directory entry and header creator"
end
