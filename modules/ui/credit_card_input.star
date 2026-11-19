# Star Standard Library: ui/credit_card_input
# Description: Smart card number formatter with auto card brand detection
# Author: Star Core Team
# Version: 1.0.0

class CreditCardInput
    property name = "credit_card_input"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: CreditCardInput>"
    end
end

function create()
    return CreditCardInput()
end

function describe()
    return "Smart card number formatter with auto card brand detection"
end
