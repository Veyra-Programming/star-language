# Star Standard Library: collections/disjoint_set
# Description: Union-Find Disjoint Set data structure with path compression
# Author: Star Core Team
# Version: 1.0.0

class DisjointSet
    property count = 0

    function element_count()
        return self.count
    end

end

function create(n)
    return DisjointSet(count = n)
end
