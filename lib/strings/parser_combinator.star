# Star Standard Library: strings/parser_combinator
# Description: Parser combinators for structured text parsing
# Author: Star Core Team
# Version: 1.0.0

class ParserCombinator
    property name = "parser_combinator"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return ParserCombinator()
end

function describe()
    return "Parser combinators for structured text parsing"
end
