def reduce_to_single_digit(n):
    while n > 9 and n not in [11, 22, 33]:
        n = sum(int(d) for d in str(n))
    return n

def total_mind_num(day):
    return reduce_to_single_digit(day)

def total_heart_num(day,month):
    reduce_to_single_digit(day+month)

def total_practical_num(birth_date):
    total = birth_date.day + birth_date.month + birth_date.year
    reduce_to_single_digit(total)

def total(birth_date):
    day = birth_date.day
    month = birth_date.month

    return {
        'mind_num':total_mind_num(day),
        'heart_num':total_heart_num(day, month),
        'practical_num':total_practical_num(birth_date)
    }