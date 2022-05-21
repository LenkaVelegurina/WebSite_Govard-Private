# проверка на цифры
def digit(password):
    for i in password:
        if i in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']:
            return True
    return False


# проверка на большие буквы
def big(password):
    for i in password:
        if i in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
                 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                 'U', 'V', 'W', 'X', 'Y', 'Z', 'А', 'Б', 'В', 'Г',
                 'Д', 'Е', 'Ё', 'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М',
                 'Н', 'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф', 'Х', 'Ц',
                 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э', 'Ю', 'Я']:
            return True
    return False


# проверка на маленькие буквы
def mini(password):
    for i in password:
        if i in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
                 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                 'u', 'v', 'w', 'x', 'y', 'z', 'а', 'б', 'в', 'г',
                 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'л', 'м',
                 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц',
                 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']:
            return True
    return False


# главная фунция проверки
def password_level(password):
    if len(password) < 8:
        return 'Недопустимый пароль'
    elif digit(password) and not mini(password) and not big(password):
        return 'Ненадежный пароль'
    elif not digit(password) and not mini(password) and big(password):
        return 'Ненадежный пароль'
    elif not digit(password) and mini(password) and not big(password):
        return 'Ненадежный пароль'
    elif not digit(password) and mini(password) and big(password):
        return 'Слабый пароль'
    elif digit(password) and mini(password) and not big(password):
        return 'Слабый пароль'
    elif digit(password) and not mini(password) and big(password):
        return 'Слабый пароль'
    else:
        return 'Надежный пароль'
