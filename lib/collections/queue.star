# Star Standard Library: collections/queue
# Description: FIFO Queue implementation with enqueue, dequeue, peek, and capacity limits
# Author: Star Core Team
# Version: 1.0.0

class Queue
    property items = []

    function enqueue(item)
        append(self.items, item)
        return len(self.items)
    end

    function size()
        return len(self.items)
    end

    function is_empty()
        return len(self.items) == 0
    end

    function peek()
        if len(self.items) == 0
        return null
        end
        return self.items[0]
    end

end

function create()
    return Queue(items = [])
end
