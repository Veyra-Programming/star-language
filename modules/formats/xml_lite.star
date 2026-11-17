# Star Standard Library: formats/xml_lite
# Description: XML tag parser and element tree builder
# Author: Star Core Team
# Version: 1.0.0

class XmlLite
    property name = "xml_lite"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return XmlLite()
end

function describe()
    return "XML tag parser and element tree builder"
end
