# Star Standard Library: ui/mentions_input
# Description: @mention and #hashtag suggestion popover input
# Author: Star Core Team
# Version: 1.0.0

class MentionsInput
    property name = "mentions_input"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: MentionsInput>"
    end
end

function create()
    return MentionsInput()
end

function describe()
    return "@mention and #hashtag suggestion popover input"
end
