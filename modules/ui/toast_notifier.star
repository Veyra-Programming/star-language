# Star Standard Library: ui/toast_notifier
# Description: Toast alert notification dispatcher
# Author: Star Core Team
# Version: 1.0.0

class ToastNotifier
    property name = "toast_notifier"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return ToastNotifier()
end

function describe()
    return "Toast alert notification dispatcher"
end
