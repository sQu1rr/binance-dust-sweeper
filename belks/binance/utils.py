def input_bool(msg, default):
    box = '[Y/n]' if default else '[y/N]'
    fullmsg = msg + ' ' + box + ' '
    value = input(fullmsg).strip().lower()

    if len(value) == 0:
        value = 'y' if default else 'n'

    while value not in ['y', 'n']:
        print('Incorrect Value (Y or N expected)')
        value = input(fullmsg).strip().lower()

    return value == 'y'
