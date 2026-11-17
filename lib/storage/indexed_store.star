# Star Standard Library: storage/indexed_store
# Description: Indexed key lookup store
# Author: Star Core Team
# Version: 1.0.0

class IndexedStore
    property name = "indexed_store"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return IndexedStore()
end

function describe()
    return "Indexed key lookup store"
end
