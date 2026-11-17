# Star Standard Library: game/state_machine
# Description: Finite State Machine with enter/exit transitions
# Author: Star Core Team
# Version: 1.0.0

class StateMachine
    property name = "state_machine"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return StateMachine()
end

function describe()
    return "Finite State Machine with enter/exit transitions"
end
