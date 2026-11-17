# Star Standard Library: collections/stack
# Description: LIFO Stack implementation with push, pop, peek, and size tracking
# Author: Star Core Team
# Version: 1.0.0

class Stack
    property items = []

    function push(item)
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
        return self.items[len(self.items) - 1]
    end

end

function create()
    return Stack(items = [])
end
