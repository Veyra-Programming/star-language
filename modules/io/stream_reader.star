# Star Standard Library: io/stream_reader
# Description: Chunked stream reading container
# Author: Star Core Team
# Version: 1.0.0

class StreamReader
    property name = "stream_reader"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return StreamReader()
end

function describe()
    return "Chunked stream reading container"
end
