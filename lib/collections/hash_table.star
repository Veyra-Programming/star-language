# Star Standard Library: collections/hash_table
# Description: Associative hash map with key hashing and bucket collision resolution
# Author: Star Core Team
# Version: 1.0.0

class HashTable
    property capacity = 16
    property count = 0

    function size()
        return self.count
    end

    function is_empty()
        return self.count == 0
    end

end

function create(cap)
    return HashTable(capacity = cap, count = 0)
end
