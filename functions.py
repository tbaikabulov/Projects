letters =  ['', 'A', 'А', 'M', 'D', 'S', 'Е', 'В', 'E', 'V', 'N', 'K', 'Д', 'I', 'И', 'М', 'R', 'Н', 'O', 'L', 'К', 'T', 'С', 'G', 'P', 'О', 'J', 'Л', 'Ю', 'B', 'Y', 'Т', 'Р', 'Г', 'П', 'C', 'F', 'Z', 'Б', 'Э', 'm', 'H', 'W', 'Ж', 'З', '']

def name(first_name, last_name):
    if first_name == None and last_name == None:
        return ''
    if last_name == None:
        return first_name
    return first_name + ' ' + last_name

#letters = ['', 'A', 'А', 'M', 'D', 'S', 'Е', 'В', 'E', 'V', 'N', 'K', 'Д', 'I', 'И', 'М', 'R', 'Н', 'O', 'L', 'К', 'T', 'С', 'G', 'P', 'О', 'J', 'Л', 'Ю', 'B', 'Y', 'Т', 'Р', 'Г', 'П', 'C', 'F', 'Z', 'Б', 'Э', 'm', 'H', 'W', 'Ж', 'З', 'U', 'i', 'a', 'd', 's', 'Ф', 'Я', '@', 'k', 'n', '.', 'v', 'p', 'b', 'g', 'X', 'Q', 'e', 'l', 'r', 'o', 'Х', 'c', 'Ч', 'f', '1', 't', 'в', 'Ш', 'w', 'а', 'У', 'y', 'u', 'и', 'м', 'е', 'Ц', 'к', 'q', 'j', '4', 'д', 'с', '…', '⚜', '🇺', '💎', '🧚', '✨', 'h', 'б', '📌', '9', '😎', '6', '𝕬', '🇮', '🌸', ':', '*', '!', '2', 'н', '🍒', 'о', '🦈', '💫', '°', '🌹', '?', '༒', '😍', '•', '💶', '🤩', '🌞', '👨', '🌶', '🐾', 'ㅤ', '🦅', 'Й', '✍', '[', '💂', '☘', 'ف', '🅢', 'ш', 'Ｓ', 'р', '-', '🎶', '"', 'л', '➤', '®', '𝓘', '—', '🔹', '$', '🌚', '🌝', '❣', '🌳', '🤍', '𝕯', '🥶', '◊', '✘', '💲', '☯', '🐈', 'Α', 'Ν', '🐻', '❤', '0', 'Δ', '<', '𝕀', '🇨', '∆', '\xa0', '🧝', '🛡', 'т', '🧜', 'э', 'г', '}', 'Š', '😈', '3', 'ⱷ', '𝗔', '☀', 'ɱ', '♍', '🍀', '🍃', ',', '✓', '⭐', '8', 'م', '🐞', '👑', '_', '👩', '●', '🤹', '🅸', 'x', 'х', '']