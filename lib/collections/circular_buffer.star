# Star Standard Library: collections/circular_buffer
# Description: Fixed-capacity ring buffer for streaming data and audio buffers
# Author: Star Core Team
# Version: 1.0.0

class CircularBuffer
    property capacity = 100
    property head = 0
    property tail = 0
    property count = 0

    function is_full()
        return self.count == self.capacity
    end

    function is_empty()
        return self.count == 0
    end

    function size()
        return self.count
    end

end

function create(cap)
    return CircularBuffer(capacity = cap, head = 0, tail = 0, count = 0)
end
