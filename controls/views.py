from django.shortcuts import render
from .models import Sector, Word, Progress
import random

def index(request):
    return render(request, 'controls/Index.html')

def users_words(users_id):
    """Returns a set with word ID's in use of current user"""
    user_and_words = Progress.objects.values_list('user_id', 'word_id', 'chance')  # Make list with tuples [(user_id, word_id),]
    users_words = []
    users_chance = []
    for x,y,z in user_and_words:
        if x == users_id:
            users_words.append(y)              # Make list with word ID's in use of current user
            users_chance.append(z)             # Make list with chances of words in use of current user
    return users_words, users_chance

def button_plus_one(request):
    """This script for button adds one new learning word for user.
    It takes random word from Word base, checks is this word unique for User,
    and makes a record in Progress Database with User ID, Word ID, and Chance
    """
    word_ids_list = Word.objects.values_list('pk', flat=True)   #Make QuerySet with all ID's in Words
    users_id = request.user.id
    message = "Sorry, we haven't new words for you, please try later"
    excludes = set()
    user_words = users_words(users_id)[0]   #Uses users_words, not users_words_chance
    while len(word_ids_list) > 0 :                # When I find the new word ID - I put the record to Progress base
        random_pick = random.choice(word_ids_list)  #Choose random word ID
        if random_pick not in user_words:
            p = Progress(user_id=users_id, word_id=random_pick)  #Write the new string in database
            p.save()
            word_obj = Word.objects.get(pk=random_pick)
            message = f"The Word {word_obj.lang1}/{word_obj.lang2} added"
            break
        else:
            user_words.remove(random_pick)
            excludes.add(random_pick)
            word_ids_list = word_ids_list.exclude(pk__in=excludes) # excludes already dropped picks
    return render(request, 'controls/Game.html', {"message":message})

def game(request):
    """Function is offer the random Word from User's base for translation, structure of letters and spaces.
    """
    users_id = request.user.id
    user_words, user_chance = users_words(users_id)
    random_pick = random.choices(user_words, weights=user_chance)
    print(random_pick)
    return render(request, 'controls/Game.html', {'random_pick':random_pick})