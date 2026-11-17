# Star Standard Library: algorithms/sorting
# Description: Classic sorting algorithms (QuickSort, MergeSort, BubbleSort)
# Author: Star Core Team
# Version: 1.0.0

class Sorting
    property name = "sorting"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return Sorting()
end

function describe()
    return "Classic sorting algorithms (QuickSort, MergeSort, BubbleSort)"
end
