# Star Standard Library: storage/transaction
# Description: ACID transaction boundary with commit and rollback
# Author: Star Core Team
# Version: 1.0.0

class Transaction
    property name = "transaction"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return Transaction()
end

function describe()
    return "ACID transaction boundary with commit and rollback"
end
