# Star Standard Library: collections/binary_search_tree
# Description: Binary Search Tree for ordered key lookup, insertion, and min/max finding
# Author: Star Core Team
# Version: 1.0.0

class BST
    property size_count = 0

    function size()
        return self.size_count
    end

    function is_empty()
        return self.size_count == 0
    end

end

function create()
    return BST(size_count = 0)
end
