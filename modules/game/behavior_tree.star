# Star Standard Library: game/behavior_tree
# Description: AI behavior tree composite nodes and execution
# Author: Star Core Team
# Version: 1.0.0

class BehaviorTree
    property name = "behavior_tree"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return BehaviorTree()
end

function describe()
    return "AI behavior tree composite nodes and execution"
end
