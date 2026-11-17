# Star Standard Library: formats/protobuf_lite
# Description: Protocol buffer varint and tag wire format utility
# Author: Star Core Team
# Version: 1.0.0

class ProtobufLite
    property name = "protobuf_lite"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return ProtobufLite()
end

function describe()
    return "Protocol buffer varint and tag wire format utility"
end
