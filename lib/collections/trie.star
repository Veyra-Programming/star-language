# Star Standard Library: collections/trie
# Description: Prefix Trie for fast string lookup, autocomplete, and dictionary queries
# Author: Star Core Team
# Version: 1.0.0

class Trie
    property word_count = 0

    function count()
        return self.word_count
    end

end

function create()
    return Trie(word_count = 0)
end
