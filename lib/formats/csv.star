# Star Standard Library: formats/csv
# Description: Comma-Separated Values parser and row generator
# Author: Star Core Team
# Version: 1.0.0

class Csv
    property name = "csv"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return Csv()
end

function describe()
    return "Comma-Separated Values parser and row generator"
end
