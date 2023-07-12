from django.shortcuts import render
from .models import Word, Progress
from django.http import HttpResponseRedirect
from .forms import AnswerForm
from django.urls import reverse
import random

# There are constants that increase or decrease value of chance to drop the word:
CORRECTANSWER = 10 # how to decrease chance for next drop with right answer (def Answer)
INCORRECTANSWER = 10 # how to increase chance for next drop with wrong answer (def Answer)

def index(request):
    return render(request, 'controls/Index.html')

def button_plus_one(request):
    """This script for button adds one new learning word for user.
    It takes random word from Word base, checks is this word unique for User,
    and makes a record in Progress Database with User ID, Word ID, and Chance
    """
    # QuerySet of All words in Base:
    word_ids_list = Word.objects.values_list('pk', flat=True)
    # QuerySet of All words of current User:
    user_words = Progress.objects.filter(user_id=request.user.id).values_list('word_id', flat=True)
    message = "Sorry, we haven't new words for you, please try later"
    excludes_words = set()
    while len(word_ids_list) > 0:
        random_pick = random.choice(word_ids_list)                      #Choose random word ID
        if random_pick not in user_words:
            p = Progress(user_id=request.user.id, word_id=random_pick)  #Write the new string in database
            p.save()
            word_obj = Word.objects.get(pk=random_pick)
            message = f"The Word {word_obj.lang1}/{word_obj.lang2} added"
            break
        else:
            excludes_words.add(random_pick)                              # excludes already dropped picks
            word_ids_list = word_ids_list.exclude(pk__in=excludes_words)
            user_words = user_words.exclude(pk__in=excludes_words)
    return HttpResponseRedirect(reverse('game') + '?message-from-button=' + message)

def game(request):
    """Function is offer the random Word from User's base for translation, structure of letters and spaces.
    """
    user_words = Progress.objects.filter(user_id=request.user.id).values_list('word_id', flat=True)
    word_chances = Progress.objects.filter(user_id=request.user.id).values_list('chance', flat=True)
    message_from_button = request.GET.get('message-from-button', '')
    message_from_answer = request.GET.get('message-from-answer', '')
    try:
        random_pick = random.choices(user_words, weights=word_chances)[0]
        # Zero here because random.choices returns a [list with one value] instead one integer
    except IndexError:
        random_pick = "You have not any words"
    lang = random.choice((1, 2))
    offered_object = Word.objects.get(id=random_pick)
    offered_word = offered_object.lang1 if lang == 1 else offered_object.lang2
    offered_sector = offered_object.sector
    offered_structure = make_word_structure(offered_object.lang2) if lang == 1 else make_word_structure(offered_object.lang1)
    offered_answer = offered_object.lang2 if lang == 1 else offered_object.lang1
    return render(request, 'controls/Game.html', {
                                    'message_from_answer':message_from_answer,
                                    'message_from_button':message_from_button,
                                    'offered_id':random_pick,
                                    'offered_answer':offered_answer,
                                    'offered_word':offered_word,
                                    'offered_sector':offered_sector,
                                    'offered_structure':offered_structure})

def make_word_structure(string):
    """Function returns the structure of word or sentence with underscores like:
    'fall in love' = '____ __ ____'
    """
    structure = ""
    for char in string:
        if char != " ":
            structure += "_"
        else:
            structure += char
    return structure

def answer(request):
    """This functions controls Users answer.
    It changes value of chance in database depending on the correctness of answer
    """
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        mess = "Cant read Input"
        if form.is_valid():
            the_answer = form.cleaned_data['answer'].lower()
            offered_answer = form.cleaned_data['offered_answer'].lower()
            offered_id = form.cleaned_data['offered_id']
            progress = Progress.objects.get(word_id=offered_id)
            if the_answer == offered_answer: # decrease chance value if the answer is correct
                progress.chance = chance_change(False, CORRECTANSWER, progress.chance)
                progress.save(update_fields=["chance"])
                mess = "Correct!"
            else:                            # increase chance value if the answer is incorrect
                progress.chance = chance_change(True, INCORRECTANSWER, progress.chance)
                progress.save(update_fields=["chance"])
                mess = "Wrong!"
        return HttpResponseRedirect(reverse('game') + '?message-from-answer=' + mess)
    else:
        form = AnswerForm()
    return render(request, 'controls/Game.html', {'form': form})

def chance_change(plus:bool, value:int, chance:int):
    """This functions controls the value of chance.
    It should be from 1 to 99
    """
    if plus == True:
        chance = chance + value if chance + value < 100 else 99
    else:
        chance = chance - value if chance - value > 0 else 1
    return chance

