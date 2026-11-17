# Star Standard Library: ai/decision_tree_lite
# Description: Binary decision stump classifier
# Author: Star Core Team
# Version: 1.0.0

class DecisionTreeLite
    property name = "decision_tree_lite"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return DecisionTreeLite()
end

function describe()
    return "Binary decision stump classifier"
end
