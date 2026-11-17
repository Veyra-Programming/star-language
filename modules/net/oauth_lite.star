# Star Standard Library: net/oauth_lite
# Description: OAuth2 authorization URL and code exchange helper
# Author: Star Core Team
# Version: 1.0.0

class OauthLite
    property name = "oauth_lite"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return OauthLite()
end

function describe()
    return "OAuth2 authorization URL and code exchange helper"
end
