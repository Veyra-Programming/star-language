# Star Standard Library: ui/otp_input
# Description: Auto-advancing segmented 4-to-6 digit OTP/PIN input
# Author: Star Core Team
# Version: 1.0.0

class OtpInput
    property name = "otp_input"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: OtpInput>"
    end
end

function create()
    return OtpInput()
end

function describe()
    return "Auto-advancing segmented 4-to-6 digit OTP/PIN input"
end
