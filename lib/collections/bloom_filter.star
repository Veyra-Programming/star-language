# Star Standard Library: collections/bloom_filter
# Description: Probabilistic Bloom Filter for set membership testing with low memory overhead
# Author: Star Core Team
# Version: 1.0.0

class BloomFilter
    property bit_size = 256
    property hash_count = 3

    function get_size()
        return self.bit_size
    end

end

function create(size)
    return BloomFilter(bit_size = size, hash_count = 3)
end
