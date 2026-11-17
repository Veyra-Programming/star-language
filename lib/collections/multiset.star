# Star Standard Library: collections/multiset
# Description: Multiset (Bag) tracking item multiplicities and element counts
# Author: Star Core Team
# Version: 1.0.0

class Multiset
    property total_elements = 0

    function size()
        return self.total_elements
    end

end

function create()
    return Multiset(total_elements = 0)
end
