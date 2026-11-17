# Star Standard Library: formats/json_utils
# Description: JSON pretty-printer, path accessor, and sanitizer
# Author: Star Core Team
# Version: 1.0.0

class JsonUtils
    property name = "json_utils"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return JsonUtils()
end

function describe()
    return "JSON pretty-printer, path accessor, and sanitizer"
end
