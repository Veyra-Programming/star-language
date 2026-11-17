# Star Standard Library: collections/linked_list
# Description: Singly Linked List node chaining and traversal container
# Author: Star Core Team
# Version: 1.0.0

class LinkedList
    property head = null
    property length = 0

    function size()
        return self.length
    end

    function is_empty()
        return self.length == 0
    end

end

function create()
    return LinkedList(head = null, length = 0)
end
