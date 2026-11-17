# Star Standard Library: collections/deque
# Description: Double-Ended Queue supporting O(1) front and back insertions
# Author: Star Core Team
# Version: 1.0.0

class Deque
    property items = []

    function push_back(item)
        append(self.items, item)
        return len(self.items)
    end

    function size()
        return len(self.items)
    end

    function is_empty()
        return len(self.items) == 0
    end

    function peek_front()
        if len(self.items) == 0
        return null
        end
        return self.items[0]
    end

    function peek_back()
        if len(self.items) == 0
        return null
        end
        return self.items[len(self.items) - 1]
    end

end

function create()
    return Deque(items = [])
end
