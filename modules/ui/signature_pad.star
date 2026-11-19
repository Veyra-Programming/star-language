# Star Standard Library: ui/signature_pad
# Description: Touch and mouse digital signature capture canvas
# Author: Star Core Team
# Version: 1.0.0

class SignaturePad
    property name = "signature_pad"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: SignaturePad>"
    end
end

function create()
    return SignaturePad()
end

function describe()
    return "Touch and mouse digital signature capture canvas"
end
