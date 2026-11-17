# Star Standard Library: collections/heap
# Description: Binary Min/Max Heap structure for priority extraction
# Author: Star Core Team
# Version: 1.0.0

class MinHeap
    property data = []

    function size()
        return len(self.data)
    end

    function is_empty()
        return len(self.data) == 0
    end

    function peek()
        if len(self.data) == 0
        return null
        end
        return self.data[0]
    end

end

function create()
    return MinHeap(data = [])
end
