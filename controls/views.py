from django.shortcuts import render
from .models import Sector, Word, Progress
from random import choice

CHANCEONSTART = 50

def sectors_list(request):
    sectors = Sector.objects.all()
    return render(request, 'controls/Sectors_List.html', {'sectors': sectors})

def words_list(request):
    words = Word.objects.all()
    return render(request, 'controls/Words_List.html', {'words': words})

def progress(request):
    progress = Progress.objects.all()
    return render(request, 'controls/Progress.html', {'progress': progress})

def game(request):
    return render(request, 'controls/Game.html')

def index(request):
    return render(request, 'controls/Index.html')

def button_plus_one(request):
    word_ids_list = Word.objects.values_list('pk', flat=True)  #Make list with all ID's in Words
    user_and_words = Progress.objects.values_list('user_id', 'word_id') #Make list with tuples [(user_id, word_id),]
    users_words = set()
    user_id = request.user.id
    message = "Sorry, we haven't new words for you, please try later"
    for x,y in user_and_words:              # Make set with word ID's in use of current user
        if x == user_id:
            users_words.add(y)
    while users_words != {}:                # When I find the new word ID - I put the record to Progress base
        random_pick = choice(word_ids_list)  #Choose random word ID
        if random_pick not in users_words:
            p = Progress(user_id=user_id, word_id=random_pick, chance=CHANCEONSTART)
            p.save()
            word_obj = Word.objects.get(pk=random_pick)
            message = f"The Word {word_obj.lang1} / {word_obj.lang2} added"
            break
        else:
            users_words.remove(random_pick)
    return render(request, 'controls/Game.html', {"message":message})