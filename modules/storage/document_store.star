# Star Standard Library: storage/document_store
# Description: NoSQL collection store with filter predicates
# Author: Star Core Team
# Version: 1.0.0

class DocumentStore
    property name = "document_store"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return DocumentStore()
end

function describe()
    return "NoSQL collection store with filter predicates"
end
