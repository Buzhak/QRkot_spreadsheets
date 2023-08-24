def len_not_null(key, value):
    if len(value) == 0:
        raise ValueError(f'Поле {key} - не может быть пустым')
    return value


def int_not_zero_or_less(key, value):
    if value <= 0:
        raise ValueError(f'Требуемая сумма {key} не может быть нулевой')
    return value
