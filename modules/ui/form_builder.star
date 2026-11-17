# Star Standard Library: ui/form_builder
# Description: Form input layout and validation state presenter
# Author: Star Core Team
# Version: 1.0.0

class FormBuilder
    property name = "form_builder"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return FormBuilder()
end

function describe()
    return "Form input layout and validation state presenter"
end
