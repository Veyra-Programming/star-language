# Star Standard Library: formats/yaml_lite
# Description: YAML key-value and list structure parser
# Author: Star Core Team
# Version: 1.0.0

class YamlLite
    property name = "yaml_lite"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return YamlLite()
end

function describe()
    return "YAML key-value and list structure parser"
end
