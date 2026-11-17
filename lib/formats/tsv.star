# Star Standard Library: formats/tsv
# Description: Tab-Separated Values parser and writer
# Author: Star Core Team
# Version: 1.0.0

class Tsv
    property name = "tsv"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return Tsv()
end

function describe()
    return "Tab-Separated Values parser and writer"
end
