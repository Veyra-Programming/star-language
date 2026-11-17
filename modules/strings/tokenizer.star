# Star Standard Library: strings/tokenizer
# Description: Word, sentence, and lexical token scanner
# Author: Star Core Team
# Version: 1.0.0

class Tokenizer
    property name = "tokenizer"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return Tokenizer()
end

function describe()
    return "Word, sentence, and lexical token scanner"
end
