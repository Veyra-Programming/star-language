# Star Standard Library: async_tools/task_queue
# Description: Async worker queue with concurrency limits
# Author: Star Core Team
# Version: 1.0.0

class TaskQueue
    property name = "task_queue"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return TaskQueue()
end

function describe()
    return "Async worker queue with concurrency limits"
end
