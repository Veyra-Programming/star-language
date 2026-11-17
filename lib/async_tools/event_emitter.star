# Star Standard Library: async_tools/event_emitter
# Description: Publish/Subscribe event emitter for custom events
# Author: Star Core Team
# Version: 1.0.0

class EventEmitter
    property name = "event_emitter"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return EventEmitter()
end

function describe()
    return "Publish/Subscribe event emitter for custom events"
end
