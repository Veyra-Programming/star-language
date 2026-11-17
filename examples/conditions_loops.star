# Conditions and Loops in Star

variable scores = [95, 82, 67, 50]

for score in scores
    if score >= 90
        show "Score " + score + ": Excellent (A)"
    else if score >= 80
        show "Score " + score + ": Very Good (B)"
    else if score >= 60
        show "Score " + score + ": Passing (C)"
    else
        show "Score " + score + ": Needs Improvement"
    end
end

show ""
show "Break and Continue Demo:"
variable n = 0
while n < 10
    n = n + 1
    if n == 2
        continue
    end
    if n == 6
        break
    end
    show "Value: " + n
end
