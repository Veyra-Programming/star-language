# Star Standard Library: io/line_reader
# Description: Line-by-line buffered text reader
# Author: Star Core Team
# Version: 1.0.0

class LineReader
    property name = "line_reader"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return LineReader()
end

function describe()
    return "Line-by-line buffered text reader"
end
