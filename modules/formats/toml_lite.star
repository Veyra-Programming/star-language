# Star Standard Library: formats/toml_lite
# Description: TOML configuration reader and key extractor
# Author: Star Core Team
# Version: 1.0.0

class TomlLite
    property name = "toml_lite"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return TomlLite()
end

function describe()
    return "TOML configuration reader and key extractor"
end
