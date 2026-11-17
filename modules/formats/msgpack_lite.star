# Star Standard Library: formats/msgpack_lite
# Description: MessagePack type prefix and packing helpers
# Author: Star Core Team
# Version: 1.0.0

class MsgpackLite
    property name = "msgpack_lite"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return MsgpackLite()
end

function describe()
    return "MessagePack type prefix and packing helpers"
end
