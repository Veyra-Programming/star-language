# Star Standard Library: ai/naive_bayes
# Description: Naive Bayes text classification word frequency model
# Author: Star Core Team
# Version: 1.0.0

class NaiveBayes
    property name = "naive_bayes"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return NaiveBayes()
end

function describe()
    return "Naive Bayes text classification word frequency model"
end
