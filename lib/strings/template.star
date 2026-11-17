# Star Standard Library: strings/template
# Description: Variable substitution and templating engine
# Author: Star Core Team
# Version: 1.0.0

class Template
    property name = "template"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return Template()
end

function describe()
    return "Variable substitution and templating engine"
end
