from django.shortcuts import render
from .models import Word, Progress
from django.http import HttpResponseRedirect
from .forms import AnswerForm
from django.urls import reverse
import random

# There are constants that increase or decrease value of chance to drop the word:
CORRECTANSWER = 7 # how to decrease chance for next drop with right answer (def Answer)
INCORRECTANSWER = 7 # how to increase chance for next drop with wrong answer (def Answer)
CHANCEONSTART = 80 # chance for drop with new words creates (inverted value is percent of learning)

def index(request):
    return render(request, 'controls/Index.html')

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
                p = Progress(user_id=user_id, word_id=random_pick, chance=CHANCEONSTART)  # Write the new string in database
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

def inverse_percentage(percent:int):
    return (-1) * percent + 101

def button_plus_one(request):
    user_id = request.user.id
    message = button_plus_word(user_id, 1)
    return HttpResponseRedirect(reverse('game') + '?message-from-button=' + message)

def button_plus_ten(request):
    user_id = request.user.id
    message = button_plus_word(user_id, 10)
    return HttpResponseRedirect(reverse('game') + '?message-from-button=' + message)

def game(request):
    """Main function for render Game Page. It offers the new word for gamer and displays buttons and statistics.
    """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))
    user_words = []
    word_chances = []
    sector_list = []
    queryset = Progress.objects.filter(user_id=request.user.id).values_list('word_id', 'chance')
    for x,y in queryset:
        user_words.append(x)
        word_for_sector = Word.objects.get(pk=x)
        sector_list.append(str(word_for_sector.sector))
        word_chances.append(y)
    sector_statistics = dictionary_with_sector_statictics(user_words, word_chances, sector_list)
    message_from_button = request.GET.get('message-from-button', '')
    message_from_answer = request.GET.get('message-from-answer', '')
    words_in_dictionary = str(len(user_words)) + "/" + str(Word.objects.count())
    try:
        random_pick = random.choices(user_words, weights=word_chances)[0]
        # Zero here because random.choices returns a [list with one value] instead one integer
    except IndexError:
        message_from_answer = "В словаре ни одного слова, давай скорее добавим, нажми кнопку слева! "
        return render(request, 'controls/Game.html', {'message_from_answer':message_from_answer,
                                                      'words_in_dictionary':words_in_dictionary})
    lang = random.choice((1, 2))
    offered_object = Word.objects.get(id=random_pick)
    offered_word = offered_object.lang1 if lang == 1 else offered_object.lang2
    offered_sector = offered_object.sector
    offered_structure = make_word_structure(offered_object.lang2) if lang == 1 else make_word_structure(offered_object.lang1)
    offered_answer = offered_object.lang2 if lang == 1 else offered_object.lang1
    learning_progress = 1
    # QuerySet hasn't method .index, so using this construction for find value by index, then invert percentage:
    for x,y in enumerate(user_words):
        if y == random_pick:
            learning_progress = inverse_percentage(word_chances[x])
    return render(request, 'controls/Game.html', {
                                    'sector_statistics':sector_statistics,
                                    'words_in_dictionary':words_in_dictionary,
                                    'message_from_answer':message_from_answer,
                                    'message_from_button':message_from_button,
                                    'offered_id':random_pick,
                                    'offered_answer':offered_answer,
                                    'offered_word':offered_word,
                                    'offered_sector':offered_sector,
                                    'offered_structure':offered_structure,
                                    'learning_progress':learning_progress})

def dictionary_with_sector_statictics(user_words:list, word_chances:list, sector_list:list):
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
    dictionary = {k:v for k,v in zip(sector_for_dict, divised_chance_for_dict)}
    return dictionary

def make_word_structure(string):
    """Function returns the structure of word or sentence with minuses like:
    'fall in love' = '---- -- ----'
    """
    structure = ""
    for char in string:
        structure += "-" if char != " " else char
    return structure

def answer(request):
    """This functions controls Users answer.
    It changes value of chance in database depending on the correctness of answer
    """
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        mess = "нет ответа"
        if form.is_valid():
            the_answer = form.cleaned_data['answer'].lower()
            offered_answer = form.cleaned_data['offered_answer'].lower()
            offered_id = form.cleaned_data['offered_id']
            progress = Progress.objects.get(word_id=offered_id)
            if the_answer == offered_answer: # decrease chance value if the answer is correct
                progress.chance = chance_change(False, CORRECTANSWER, progress.chance)
                progress.save(update_fields=["chance"])
                mess = "Верно!"
            else:                            # increase chance value if the answer is incorrect
                progress.chance = chance_change(True, INCORRECTANSWER, progress.chance)
                progress.save(update_fields=["chance"])
                mess = f"Неправильно! Ответ: {offered_answer}"
        return HttpResponseRedirect(reverse('game') + '?message-from-answer=' + mess)
    else:
        form = AnswerForm()
    return render(request, 'controls/Game.html', {'form': form})

def chance_change(plus:bool, value:int, chance:int):
    """This functions controls the value of chance.
    It should be from 1 to 99
    """
    if plus == True:
        chance = chance + value if chance + value < 99 else 99
    else:
        chance = chance - value if chance - value > 1 else 1
    return chance

