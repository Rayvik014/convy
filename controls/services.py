from .models import Word, Progress
import random

# There are some constants:
CORRECT_ANSWER = 7  # how to decrease chance for next drop with right answer (def Answer)
INCORRECT_ANSWER = 7  # how to increase chance for next drop with wrong answer (def Answer)
CHANCE_ON_START = 80  # chance for drop with new words creates (inverted value is percent of learning)


def count_words_in_dictionary(user_id):
    words_in_dict = str(Progress.objects.filter(user_id=user_id).count()) + "/" + str(Word.objects.count())
    return words_in_dict


def count_percent_of_learning(user_id):
    percent_of_learning = 0
    percents = Progress.objects.filter(user_id=user_id).values_list('chance', flat=True)
    if percents:
        for x, y in enumerate(percents):
            percent_of_learning += y
        percent_of_learning = inverse_percentage(percent_of_learning // (x + 1))
    return percent_of_learning


def make_words_chances_sector_lists(user_id):
    user_words = []
    word_chances = []
    sector_list = []
    queryset = Progress.objects.filter(user_id=user_id).values_list('word_id', 'chance')
    for x, y in queryset:
        user_words.append(x)
        word_for_sector = Word.objects.get(pk=x)
        sector_list.append(str(word_for_sector.sector))
        word_chances.append(y)
    return user_words, word_chances, sector_list


def get_offering_object(random_pick):
    lang = random.choice((1, 2))
    offered_object = Word.objects.get(id=random_pick)
    offered_word = offered_object.lang1 if lang == 1 else offered_object.lang2
    offered_sector = offered_object.sector
    offered_structure = make_word_structure(offered_object.lang2) if lang == 1 else (
        make_word_structure(offered_object.lang1))
    offered_answer = offered_object.lang2 if lang == 1 else offered_object.lang1
    return offered_word, offered_sector, offered_structure, offered_answer


def change_progress_value(the_answer, offered_answer, offered_id):
    progress = Progress.objects.get(word_id=offered_id)
    if the_answer == offered_answer:  # decrease chance value if the answer is correct
        progress.chance = chance_change(False, CORRECT_ANSWER, progress.chance)
        progress.save(update_fields=["chance"])
        mess = "Верно!"
    else:  # increase chance value if the answer is incorrect
        progress.chance = chance_change(True, INCORRECT_ANSWER, progress.chance)
        progress.save(update_fields=["chance"])
        mess = f"Неправильно! Ответ: {offered_answer}"
    return mess


def button_plus_word(user_id, count_of_words):
    """This script for button adds one new learning word for user.
    It takes random word from Word base, checks is this word unique for User,
    and makes a record in Progress Database with User ID, Word ID, and Chance
    """
    message, message2 = "", ""
    for i in range(count_of_words):
        # QuerySet of All words (word_ids) in Base:
        word_ids_list = Word.objects.values_list('pk', flat=True)
        # QuerySet of All words (word_ids) of current User:
        user_words = Progress.objects.filter(user_id=user_id).values_list('word_id', flat=True)
        excludes_words = set()
        while len(word_ids_list) > 0:
            random_pick = random.choice(word_ids_list)  # Choose random word ID
            if random_pick not in user_words:
                p = Progress(user_id=user_id, word_id=random_pick,
                             chance=CHANCE_ON_START)  # Write the new string in database
                p.save()
                word_obj = Word.objects.get(pk=random_pick)
                message2 += f"Добавлено слово: {word_obj.lang1}/{word_obj.lang2}\n"
                break
            else:
                excludes_words.add(random_pick)  # excludes already dropped picks
                word_ids_list = word_ids_list.exclude(pk__in=excludes_words)
                user_words = user_words.exclude(pk__in=excludes_words)
    message = "Нет больше новых слов" if message2 == "" else message2
    return message


def inverse_percentage(percent: int):
    return (-1) * percent + 101


def dictionary_with_sector_statictics(user_words: list, word_chances: list, sector_list: list):
    """This function calculate progress percent for each sector.
    :param user_words: list[] with word ID's using by player
    :param word_chances: list[] with chances of drop by each word
    :param sector_list: List[] with names of sectors using by player
    :return: Dictionary with progress values by sectors
    """
    sector_for_dict = []
    chance_for_dict = []
    quantity_for_dict = []
    divised_chance_for_dict = []
    for i in range(len(user_words)):
        if sector_list[i] not in sector_for_dict:
            sector_for_dict.append(sector_list[i])
            chance_for_dict.append(word_chances[i])
            quantity_for_dict.append(1)
            divised_chance_for_dict.append(inverse_percentage(word_chances[i]))
        else:
            k = sector_for_dict.index(sector_list[i])
            chance_for_dict[k] += word_chances[i]
            quantity_for_dict[k] += 1
            divised_chance_for_dict[k] = inverse_percentage(chance_for_dict[k] // quantity_for_dict[k])
    dictionary = {k: v for k, v in zip(sector_for_dict, divised_chance_for_dict)}
    return dictionary


def make_word_structure(string):
    """Function returns the structure of word or sentence with minuses like:
    'fall in love' = '---- -- ----'
    """
    structure = ""
    for char in string:
        structure += "-" if char != " " else char
    return structure


def chance_change(plus: bool, value: int, chance: int):
    """This functions controls the value of chance.
    It should be from 1 to 99
    """
    if plus:
        chance = chance + value if chance + value < 99 else 99
    else:
        chance = chance - value if chance - value > 1 else 1
    return chance
