# Star Standard Library: ui/review_card
# Description: Customer testimonial and review card with star rating and verified badge
# Author: Star Core Team
# Version: 1.0.0

class ReviewCard
    property name = "review_card"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: ReviewCard>"
    end
end

function create()
    return ReviewCard()
end

function describe()
    return "Customer testimonial and review card with star rating and verified badge"
end
