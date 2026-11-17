# Star Standard Library: strings/unicode_helper
# Description: Unicode code point utilities and length validation
# Author: Star Core Team
# Version: 1.0.0

class UnicodeHelper
    property name = "unicode_helper"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return UnicodeHelper()
end

function describe()
    return "Unicode code point utilities and length validation"
end
