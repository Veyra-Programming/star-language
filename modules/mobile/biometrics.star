# Star Standard Library: mobile/biometrics
# Description: Biometric face and fingerprint availability checker
# Author: Star Core Team
# Version: 1.0.0

class Biometrics
    property name = "biometrics"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return Biometrics()
end

function describe()
    return "Biometric face and fingerprint availability checker"
end
