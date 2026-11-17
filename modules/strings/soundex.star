# Star Standard Library: strings/soundex
# Description: Phonetic phonetic encoding algorithm
# Author: Star Core Team
# Version: 1.0.0

class Soundex
    property name = "soundex"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return Soundex()
end

function describe()
    return "Phonetic phonetic encoding algorithm"
end
