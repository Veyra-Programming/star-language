# Star Standard Library: crypto/vigenere
# Description: Polyalphabetic Vigenere cipher
# Author: Star Core Team
# Version: 1.0.0

class Vigenere
    property name = "vigenere"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return Vigenere()
end

function describe()
    return "Polyalphabetic Vigenere cipher"
end
