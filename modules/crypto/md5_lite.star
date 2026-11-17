# Star Standard Library: crypto/md5_lite
# Description: MD5 digest simulation helper
# Author: Star Core Team
# Version: 1.0.0

class Md5Lite
    property name = "md5_lite"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return Md5Lite()
end

function describe()
    return "MD5 digest simulation helper"
end
