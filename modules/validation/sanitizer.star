# Star Standard Library: validation/sanitizer
# Description: HTML tag stripping and XSS character sanitizer
# Author: Star Core Team
# Version: 1.0.0

class Sanitizer
    property name = "sanitizer"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return Sanitizer()
end

function describe()
    return "HTML tag stripping and XSS character sanitizer"
end
