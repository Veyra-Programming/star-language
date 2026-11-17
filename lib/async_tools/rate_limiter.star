# Star Standard Library: async_tools/rate_limiter
# Description: Token bucket rate limiting algorithm
# Author: Star Core Team
# Version: 1.0.0

class RateLimiter
    property name = "rate_limiter"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return RateLimiter()
end

function describe()
    return "Token bucket rate limiting algorithm"
end
