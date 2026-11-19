# Star Standard Library: ui/comment_thread
# Description: Nested hierarchical discussion comment thread with replies
# Author: Star Core Team
# Version: 1.0.0

class CommentThread
    property name = "comment_thread"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: CommentThread>"
    end
end

function create()
    return CommentThread()
end

function describe()
    return "Nested hierarchical discussion comment thread with replies"
end
