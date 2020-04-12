import numpy as np


def game_core_v1(number, start, end):
    '''Просто угадываем на random, никак не используя информацию о больше или меньше.
       Функция принимает загаданное число и возвращает число попыток'''
    count = 0
    while True:
        count+=1
        predict = np.random.randint(start,end) # предполагаемое число
        if number == predict: 
            return(count) # выход из цикла, если угадали
        
        
def score_game(game_core, start, end):
    '''Запускаем игру 1000 раз, чтобы узнать, как быстро игра угадывает число'''
    count_ls = []
    np.random.seed(1)  # фиксируем RANDOM SEED, чтобы ваш эксперимент был воспроизводим!
    random_array = np.random.randint(start, end, size=1000)
    for number in random_array:
        count_ls.append(game_core(number, start, end))
    score = int(np.mean(count_ls))
    print(f"Алгоритм {game_core} угадывает число в среднем за {score} попыток")
    return(score)


def game_core_v2(number, start, end):
    '''Сначала устанавливаем любое random число, а потом уменьшаем или увеличиваем его в зависимости от того, больше оно или меньше нужного.
       Функция принимает загаданное число и возвращает число попыток'''
    count = 1
    predict = np.random.randint(start,end)
    while number != predict:
        count+=1
        if number > predict: 
            predict += 1
        elif number < predict: 
            predict -= 1
    return(count) # выход из цикла, если угадали


def game_core_v3(number, start, end):
    '''Берем входной интервал [start,end), и в цикле сравниваем его середину с загаданным 
       числом. Если число справа, то заменяем начало интервала его серединой.
       Если число слева, то заменяем конец интервала серединой. Повторяем пока 
       середина не совпадет с загаданным числом'''
    
    def middle(start, end):
        return start + (end-start)//2

    count = 0
    while True:
        predict = middle(start, end)      
        count += 1
        if number < predict:
            end = predict
        elif number > predict:
            start = predict
        else:
            break                    
    return(count)


# запускаем
start = 1
end = 101

score_game(game_core_v1, start, end)
score_game(game_core_v2, start, end)
score_game(game_core_v3, start, end)
