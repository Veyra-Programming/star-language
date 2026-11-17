# Star Standard Library: storage/key_value_store
# Description: Key-value persistent storage engine with serialisation
# Author: Star Core Team
# Version: 1.0.0

class KeyValueStore
    property name = "key_value_store"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return KeyValueStore()
end

function describe()
    return "Key-value persistent storage engine with serialisation"
end
