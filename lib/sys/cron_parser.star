# Star Standard Library: sys/cron_parser
# Description: Cron schedule expression parser and evaluation
# Author: Star Core Team
# Version: 1.0.0

class CronParser
    property name = "cron_parser"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return CronParser()
end

function describe()
    return "Cron schedule expression parser and evaluation"
end
