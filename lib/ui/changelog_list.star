# Star Standard Library: ui/changelog_list
# Description: Software version changelog list with release badges
# Author: Star Core Team
# Version: 1.0.0

class ChangelogList
    property name = "changelog_list"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: ChangelogList>"
    end
end

function create()
    return ChangelogList()
end

function describe()
    return "Software version changelog list with release badges"
end
