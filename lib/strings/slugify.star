# Star Standard Library: strings/slugify
# Description: URL slug generator converting text to kebab-case
# Author: Star Core Team
# Version: 1.0.0

class Slugify
    property name = "slugify"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return Slugify()
end

function describe()
    return "URL slug generator converting text to kebab-case"
end
