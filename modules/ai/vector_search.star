# Star Standard Library: ai/vector_search
# Description: Cosine similarity and Euclidean distance vector retrieval
# Author: Star Core Team
# Version: 1.0.0

class VectorSearch
    property name = "vector_search"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return VectorSearch()
end

function describe()
    return "Cosine similarity and Euclidean distance vector retrieval"
end
