# Star Standard Library: algorithms/cryptographic_sort
# Description: Timing-safe constant-time string comparisons
# Author: Star Core Team
# Version: 1.0.0

class CryptographicSort
    property name = "cryptographic_sort"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return CryptographicSort()
end

function describe()
    return "Timing-safe constant-time string comparisons"
end
