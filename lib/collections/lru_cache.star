# Star Standard Library: collections/lru_cache
# Description: Least-Recently-Used (LRU) Cache eviction policy container
# Author: Star Core Team
# Version: 1.0.0

class LRUCache
    property capacity = 10
    property size_count = 0

    function get_capacity()
        return self.capacity
    end

    function size()
        return self.size_count
    end

end

function create(cap)
    return LRUCache(capacity = cap, size_count = 0)
end
