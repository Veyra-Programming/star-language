# Star Standard Library: ui/faq_accordion
# Description: Frequently asked questions accordion with search highlight
# Author: Star Core Team
# Version: 1.0.0

class FaqAccordion
    property name = "faq_accordion"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: FaqAccordion>"
    end
end

function create()
    return FaqAccordion()
end

function describe()
    return "Frequently asked questions accordion with search highlight"
end
