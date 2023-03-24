import random


def roll_d4():
    # Подбрасываем четырехгранную кость
    result = random.randint(1, 4)
    return result

def roll_d6():
    # Подбрасываем шестигранную кость
    result = random.randint(1, 6)
    return result

def roll_d8():
    # Подбрасываем восьмигранную кость
    result = random.randint(1, 8)
    return result

def roll_d12():
    # Подбрасываем двенадцатигранную кость
    result = random.randint(1, 12)
    return result

def roll_d16():
    # Подбрасываем шестнадцатигранную кость
    result = random.randint(1, 16)
    return result

def roll_d20():
    # Подбрасываем двадцатигранную кость
    result = random.randint(1, 20)
    return result