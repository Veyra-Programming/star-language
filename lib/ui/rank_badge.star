# Star Standard Library: ui/rank_badge
# Description: Gamified gold, silver, bronze ranking badge with ribbon
# Author: Star Core Team
# Version: 1.0.0

class RankBadge
    property name = "rank_badge"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: RankBadge>"
    end
end

function create()
    return RankBadge()
end

function describe()
    return "Gamified gold, silver, bronze ranking badge with ribbon"
end
