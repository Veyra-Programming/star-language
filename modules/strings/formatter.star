# Star Standard Library: strings/formatter
# Description: Data formatting for numbers, currency, and byte sizes
# Author: Star Core Team
# Version: 1.0.0

class Formatter
    property name = "formatter"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return Formatter()
end

function describe()
    return "Data formatting for numbers, currency, and byte sizes"
end
