# Star Standard Library: collections/priority_queue
# Description: Priority Queue with ordered item scheduling
# Author: Star Core Team
# Version: 1.0.0

class PriorityQueue
    property entries = []

    function size()
        return len(self.entries)
    end

    function is_empty()
        return len(self.entries) == 0
    end

end

function create()
    return PriorityQueue(entries = [])
end
