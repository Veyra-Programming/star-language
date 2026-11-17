# Star Standard Library: io/file_watcher
# Description: File system change notification events
# Author: Star Core Team
# Version: 1.0.0

class FileWatcher
    property name = "file_watcher"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return FileWatcher()
end

function describe()
    return "File system change notification events"
end
