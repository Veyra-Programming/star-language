# Star Standard Library: net/websocket
# Description: WebSocket frame builder and opcode helper
# Author: Star Core Team
# Version: 1.0.0

class Websocket
    property name = "websocket"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return Websocket()
end

function describe()
    return "WebSocket frame builder and opcode helper"
end
