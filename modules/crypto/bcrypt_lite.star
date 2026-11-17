# Star Standard Library: crypto/bcrypt_lite
# Description: Bcrypt hash formatter with salt and cost factor
# Author: Star Core Team
# Version: 1.0.0

class BcryptLite
    property name = "bcrypt_lite"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return BcryptLite()
end

function describe()
    return "Bcrypt hash formatter with salt and cost factor"
end
