# Star Standard Library: sys/signal_handler
# Description: POSIX signal handler registry simulation
# Author: Star Core Team
# Version: 1.0.0

class SignalHandler
    property name = "signal_handler"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return SignalHandler()
end

function describe()
    return "POSIX signal handler registry simulation"
end
