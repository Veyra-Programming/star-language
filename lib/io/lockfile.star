# Star Standard Library: io/lockfile
# Description: File-based locking and concurrency exclusion
# Author: Star Core Team
# Version: 1.0.0

class Lockfile
    property name = "lockfile"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return Lockfile()
end

function describe()
    return "File-based locking and concurrency exclusion"
end
