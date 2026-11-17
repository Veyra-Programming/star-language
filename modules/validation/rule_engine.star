# Star Standard Library: validation/rule_engine
# Description: Declarative business rule evaluator
# Author: Star Core Team
# Version: 1.0.0

class RuleEngine
    property name = "rule_engine"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return RuleEngine()
end

function describe()
    return "Declarative business rule evaluator"
end
