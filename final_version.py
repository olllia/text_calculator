# сложность: база 3 балла, усложнения: 3, 4, 5, 10 -- баллы 3+3+1+1, итог: 11
import time  # для имитации ожидания

number_to_word = {
    0: 'ноль',
    1: 'один',
    2: 'два',
    3: 'три',
    4: 'четыре',
    5: 'пять',
    6: 'шесть',
    7: 'семь',
    8: 'восемь',
    9: 'девять',
    10: 'десять',
    11: 'одиннадцать',
    12: 'двенадцать',
    13: 'тринадцать',
    14: 'четырнадцать',
    15: 'пятнадцать',
    16: 'шестнадцать',
    17: 'семнадцать',
    18: 'восемнадцать',
    19: 'девятнадцать',
    20: 'двадцать',
    30: 'тридцать',
    40: 'сорок',
    50: 'пятьдесят',
    60: 'шестьдесят',
    70: 'семьдесят',
    80: 'восемьдесят',
    90: 'девяносто',
    100: 'сто',
    200: 'двести',
    300: 'триста',
    400: 'четыреста',
    500: 'пятьсот',
    600: 'шестьсот',
    700: 'семьсот',
    800: 'восемьсот',
    900: 'девятьсот'
}

word_to_number = {value: key for key, value in number_to_word.items()}  # создаем перевернутый словарь

operations_dict = {
    'плюс': '+',
    'минус': '-',
    'умножить на': '*',
    'разделить на': '/',
    'скобка открывается': '(',
    'скобка закрывается': ')'
}


# функция ищет в тексте (строка) слова относящиеся к арифметаческим операциям и заменяет их прямо в тексте на сами операции
def find_and_replace_operations(text):
    replaced_text = text  # делаем копию текста
    for operation in operations_dict.keys():  # пробегаемся по каждой операции в ключах словаря с операциями
        if operation in replaced_text:
            replaced_text = replaced_text.replace(operation, operations_dict[
                operation])  # если есть совпадения, то заменяем словесную запись операций на математическую
    return replaced_text


# функция разделяет число на десятые, сотые, тысячные (разряды) Например 1234 --> [1000, 200, 30, 4]
def separate_number(num):
    # Проверка на ноль, чтобы функция не интрепретировала str(0) как пустую строку
    # Поэтому без этого когда в ответе получался ноль калькулятор не выводил его
    if num == 0:
        return [0]
    num_parts = []  # задаем список для хранения разрядов
    # если остаток от деления не равен исходному числу
    if num % 1000 != num:
        # то берем целую часть от деления и добавляем в список
        # например от 1234 берем 1000 и записываем в список
        num_parts.append(num - num % 1000)
        num = num % 1000  # далее будем работать с остатком от деления, т.е. 234

    if num % 100 != num:
        num_parts.append(num - num % 100)  # тут добавляется 200
        num = num % 100  # работаем далее с 34

    if num % 10 != num and num > 20:  # т.к. не хотим чтобы числа 10-19 выводились как например "десять девять" и тд
        num_parts.append(num - num % 10)
        num = num % 10  # затем остаеется 4
    if num != 0:
        num_parts.append(num)  # добавляем ее в конец списка
    return num_parts


# функция преобразует число в текстовое написание
def translate_number_to_words(num):
    words = []  # создаем список в котором будет храниться результат
    if num < 0:
        words.append("минус")
        num *= -1
    for num_part in separate_number(num):  # вызываем функцию separate_number, которая разделяет число на разряды
        # Запускаем цикл по каждому разряду
        if num_part >= 1000:  # если разряд больше или равен 1000, тогда нужно с тысячами разобраться отдельно
            thousands_parts = separate_number(
                int(num_part / 1000))  # делим на 1000. (например 576000/1000 = 576, дальше работаем с этим числом)
            # separate_number вернет [500, 70, 6]
            for t_part in thousands_parts:  # для каждого числа являющегося частью тысяч
                if t_part != thousands_parts[-1]:  # если это не последнее число
                    words.append(number_to_word[t_part])  # то просто преобразуем его в текст
                else:  # а если последнее, то к нему надо добавить 'тысяч' в правильном падеже
                    if t_part == 1:
                        words.append("одна тысяча")
                    elif t_part == 2:
                        words.append("две тысячи")
                    elif 3 <= thousands_parts[-1] <= 4:
                        words.append(number_to_word[t_part] + " тысячи")
                    elif 5 <= thousands_parts[-1] <= 999:
                        words.append(number_to_word[t_part] + " тысяч")
                    else:
                        return 'больше девятьсот тысяч девятьсот девяносто девять'
        else:  # если число меньше 1000, то просто каждую часть преобразуем в текст и добавляем к результирующей строке
            words.append(number_to_word[num_part])
    return ' '.join(words)


# функция проверяет, является ли символ арифметической операцией
def is_operation(symbol):
    return symbol in operations_dict.values()


# функция проверяет, является ли слово текстовым написанием числа
def is_text_number(word):
    return word in number_to_word.values()

# функция проверяет является ли слово числом
def is_number(word):
    try:
        int(word)
        return True
    except:
        return False


# функция разбирает строку и превращает ее в математическое выражение
def parse(text):
    text = find_and_replace_operations(text)  # применяем к строке функцию find_and_replace_operations
    elements_list = text.split()  # преобразуем строку в список
    # цикл ниже пробегается по списку слов и если находит в нем слова соответствующие числам,
    # то преобразует их в числа и заменяет в списке
    # например, список ['(', 'пятьдесят', 'пять', '+', 'два', ')', '*', 'три', '-', '-', 'один']
    # преобразуется в список ['(', 50, 5, '+', 2, ')', '*', 3, '-', '-', 1]
    for index in range(len(elements_list)):
        if len(elements_list) > index and is_text_number(elements_list[index]):
            elements_list[index] = word_to_number[elements_list[index]]

    # цикл ниже пробегается по списку и если находит в нем соседние числа, то складнывает их.
    # а так же, если находит два оператора подряд, второй из них "-", и после него число,
    # то делает это число отрицательным и удаляет "-" из списка
    # например, на предыдущем шаге был список ['(', 50, 5, '+', 2, ')', '*', 3, '-', '-', 1]
    # он будет преобразован в список ['(', 55, '+', 2, ')', '*', 3, '-', -1]
    while True:
        src_elements_list = elements_list.copy()
        for index in range(len(elements_list)):
            if len(elements_list) > index + 1 and is_number(elements_list[index]) and is_number(
                    elements_list[index + 1]):
                elements_list[index] += elements_list[index + 1]
                del elements_list[index + 1]
            if len(elements_list) > index + 1 \
                    and elements_list[index] == "-" \
                    and (index == 0 or is_operation(elements_list[index - 1])) and is_number(elements_list[index + 1]):
                elements_list[index + 1] = elements_list[index + 1] * -1
                del elements_list[index]
        if elements_list == src_elements_list:
            break
    return elements_list

# функция реализует польскую инверсную запись числа (постфиксная нотация)
def convert_to_reverse_polish_notation(math_expression):
    operations_priority = {
        '*': 3,
        '/': 3,
        '+': 2,
        '-': 2,
        '(': 1
    }

    operations_stack = []  # создаем пустой стек где будем хранить операторы (стек это как список, но более ограниченный по функционалу)
    rpn_expression = []  # создаем пустой список для результата
    for token in math_expression:  # token это просто элемент мат. выражения
        if is_number(token):
            rpn_expression.append(token)  # если это число, то добавляем его в результирующий список
        elif token == "(":
            operations_stack.append(token)  # если открывающаяся скобка, то кладем ее в стек с операциями
        elif token == ")":
            operation = operations_stack.pop()  # достаем верхний элемент из стека
            while operation != "(":  # до тех пор пока не дойдем до открывающейся скобки
                rpn_expression.append(operation)  # добавляем верхний элемент стека в итоговый список
                operation = operations_stack.pop()  # достаем следующий элемент стека, чтобы на следующей итерации проверить его
        elif is_operation(token):  # если это операция, то
            # пока стек не пустой и приоретеность последней операции больше или равна приоритетности токена
            while len(operations_stack) > 0 and operations_priority[operations_stack[-1]] >= operations_priority[token]:
                rpn_expression.append(operations_stack.pop())  # достаем верхний элемент из стека и кладем его в итоговый список
            operations_stack.append(token)
    while len(operations_stack) > 0:
        rpn_expression.append(operations_stack.pop())  # если что-то осталось в стеке операций, то добавить в rpn_expression
    return rpn_expression

# print(convert_to_reverse_polish_notation(['(', 155, '+', 2, ')', '*', 3, '-', -1]))

# функция вычисляет выражение, представленное в виде польской инверсии
def evaluate_reverse_polish_notation(rpn_expression):
    numbers_stack = []  # создаем пустой стек, куда будем класть результат
    for token in rpn_expression:
        if is_number(token):  # если элемент выр-я является числом, то добавляем в стек
            numbers_stack.append(token)
        elif is_operation(token):  # если же операцией
            second_num = numbers_stack.pop()  # достаем второе число
            first_num = numbers_stack.pop()  # достаем первое число
            tmp_res = eval(str(first_num) + token + str(second_num))  # составляем строку из двух чисел и оператора между ними и передаем в функцию eval(),
            # которая должна выполнить выражение записанное в строке и сразу вернуть числовой результат
            numbers_stack.append(tmp_res)  # записываем промежуточный результат в обратно стек
    return numbers_stack.pop()  # после цикла в стеке остается всего один элемент, это и есть результат расчета, достаем его и помещаем в return

# проверяет корректность введенного текста
def validate(text):
    # проверка что количество открывающихся и закрывающихся скобок равно
    open_parenthesis_cout = text.count('скобка открывается')
    close_parenthesis_cout = text.count('скобка закрывается')
    if open_parenthesis_cout != close_parenthesis_cout:
        return False, 'Количество открывающихся скобок: ' + str(
            open_parenthesis_cout) + ', а количество закрывающихся: ' + str(close_parenthesis_cout)
    return True, ''


# основная функция вычисления
def calc(text):
    print(text)
    text = text.lower()  # чтобы регистр не учитывался
    is_ok, err = validate(text)  # проверка наличия ошибки со скобками
    if not is_ok:
        return 'Ошибка! ' + err
    math_expression_list = parse(text)  # разбираем строку и превращаем в мат выражение
    rpn_expression_list = convert_to_reverse_polish_notation(math_expression_list)  # применяем польскую нотацию
    result_num = int(evaluate_reverse_polish_notation(rpn_expression_list))  # вычисляем
    return translate_number_to_words(result_num)  # переводим получившийся результат в текстовое написание


print("Это текстовый кальтулятор. "
      "Введите, пожалуйста, математическое выражение в тексте:")
input_string = input()

test_text = "Cкобка открывается сто пятьдесят пять плюс два скобка закрывается умножить на три минус минус один"
test_text2 = "девятьсот девяносто девять умножить на девятьсот девяносто девять"
test_text3 = "два умножить на ноль"
test_text4 = "минус семь минус минус один"
test_text5 = "семь разделить на три"
test_text6 = "скобка открывается сто пятьдесят пять плюс два скобка закрывается умножить на десять минус минус один"
test_text8 = "скобка открывается скобка открывается пять плюс два скобка закрывается умножить на скобка открывается один плюс два скобка закрывается скобка закрывается"
test_text9 = "скобка открывается скобка открывается пять плюс два скобка закрывается умножить на скобка открывается один плюс два скобка закрывается"

# print(test_text)
print("секундочку, провожу сложные математические вычисления...")
time.sleep(2)
print("еще немного...")
time.sleep(1)
print("очень стараюсь...")
time.sleep(1)
print("Результат: ", calc(input_string))
