# Star Standard Library: io/stream_writer
# Description: Buffered stream output sink
# Author: Star Core Team
# Version: 1.0.0

class StreamWriter
    property name = "stream_writer"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return StreamWriter()
end

function describe()
    return "Buffered stream output sink"
end
