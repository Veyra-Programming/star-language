# Star Standard Library: strings/ascii_table
# Description: ASCII art table layout and border rendering
# Author: Star Core Team
# Version: 1.0.0

class AsciiTable
    property name = "ascii_table"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return AsciiTable()
end

function describe()
    return "ASCII art table layout and border rendering"
end
