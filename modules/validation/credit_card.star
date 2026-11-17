# Star Standard Library: validation/credit_card
# Description: Luhn algorithm payment card number validator
# Author: Star Core Team
# Version: 1.0.0

class CreditCard
    property name = "credit_card"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return CreditCard()
end

function describe()
    return "Luhn algorithm payment card number validator"
end
