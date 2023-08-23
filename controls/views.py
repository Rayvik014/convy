from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User, Group
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth import get_user_model, login, logout
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from .forms import AnswerForm, LoginForm, RegistrationForm, MyPasswordResetForm
import random
import services


def index(request):
    """Controls render of main page"""
    user_id = request.user.id
    message_auth = request.GET.get('message-auth', '')
    return render(request, 'controls/Index.html', {'message_auth': message_auth,
                                                   'words_in_dict': services.count_words_in_dictionary(user_id),
                                                   'percent_of_learning': services.count_percent_of_learning(user_id)})


def button_plus_one(request):
    """Action fo button '+1 word'"""
    user_id = request.user.id
    message = services.button_plus_word(user_id, 1)
    return HttpResponseRedirect(reverse('game') + '?message-from-button=' + message)


def button_plus_ten(request):
    """Action fo button '+10 words'"""
    user_id = request.user.id
    message = services.button_plus_word(user_id, 10)
    return HttpResponseRedirect(reverse('game') + '?message-from-button=' + message)


def game(request):
    """Main function for render Game Page. It offers the new word for gamer and displays buttons and statistics.
    """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))
    user_id = request.user.id
    user_words, word_chances, sector_list = services.make_words_chances_sector_lists(user_id)

    sector_statistics = services.dictionary_with_sector_statictics(user_words, word_chances, sector_list)
    words_in_dictionary = services.count_words_in_dictionary(user_id)
    message_from_button = request.GET.get('message-from-button', '')
    message_from_answer = request.GET.get('message-from-answer', '')

    try:
        random_pick = random.choices(user_words, weights=word_chances)[0]
        # Zero here because random.choices returns a [list with one value] instead one integer
    except IndexError:
        message_from_answer = "В словаре ни одного слова, давай скорее добавим, нажми кнопку слева! "
        return render(request, 'controls/Game.html', {'message_from_answer': message_from_answer,
                                                      'words_in_dictionary': words_in_dictionary})

    offered_word, offered_sector, offered_structure, offered_answer = services.get_offering_object(random_pick)

    learning_progress = 1
    # QuerySet hasn't method .index, so using this construction for find value by index, then invert percentage:
    for x, y in enumerate(user_words):
        if y == random_pick:
            learning_progress = services.inverse_percentage(word_chances[x])

    return render(request, 'controls/Game.html', {
        'sector_statistics': sector_statistics,
        'words_in_dictionary': words_in_dictionary,
        'message_from_answer': message_from_answer,
        'message_from_button': message_from_button,
        'offered_id': random_pick,
        'offered_answer': offered_answer,
        'offered_word': offered_word,
        'offered_sector': offered_sector,
        'offered_structure': offered_structure,
        'learning_progress': learning_progress})


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
            mess = services.change_progress_value(the_answer, offered_answer, offered_id)
        return HttpResponseRedirect(reverse('game') + '?message-from-answer=' + mess)
    else:
        form = AnswerForm()
        return render(request, 'controls/Game.html', {'form': form})


class EmailBackend(ModelBackend):
    """This class replaces standard ModelBackend class and uses Email for authorization instead name"""

    def authenticate(self, request, username=None, password=None, **kwargs):
        user_model = get_user_model()
        try:
            user = user_model.objects.get(email=username)
        except user_model.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None


def my_login(request):
    """This custom login function reacts on clicking button Log-In"""
    message = "Введите адрес электронной почты и пароль"
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = EmailBackend().authenticate(request, username=form.cleaned_data['email_value'].lower(),
                                               password=form.cleaned_data['password_value'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                else:
                    message = "Аккаунт заблокирован"
            else:
                message = "Неправильный адрес электронной почты или пароль"
        return HttpResponseRedirect(reverse('index') + '?message-auth=' + message)
    else:
        form = LoginForm()
        return render(request, 'controls/Index.html', {'form': form})


def my_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def registration(request):
    """This function is reacted on button Registration. It creates a new user"""
    message = ""
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user_name = form.cleaned_data['user_name']
            user_email = form.cleaned_data['user_email'].lower()
            user_password_1 = form.cleaned_data['user_password_1']
            user_password_2 = form.cleaned_data['user_password_2']
            if user_password_1 == user_password_2:
                if user_email not in User.objects.values_list('email', flat=True):
                    User.objects.create_user(user_name, user_email, user_password_1)
                    user = EmailBackend().authenticate(request, username=user_email,
                                                       password=user_password_1)
                    group = Group.objects.get(name="Gamers")
                    user.groups.add(group)
                    login(request, user)
                    return HttpResponseRedirect(reverse('index'))
                else:
                    message = "Пользователь с такой электронной почтой уже зарегистрирован!"
            else:
                message = "Пароли не совпадают, попробуйте снова!"
        else:
            message = form.errors
    form = RegistrationForm()
    return render(request, 'registration/registration.html', {'form': form,
                                                              'message': message})


class MyPasswordResetView(PasswordResetView):
    """Overriding the class for using custom form"""
    form_class = MyPasswordResetForm

    def form_valid(self, form):
        email = form.cleaned_data.get('email', '').lower()
        try:
            user = get_user_model().objects.get(email=email)
        except get_user_model().DoesNotExist:
            user = None
        if user is None:
            return HttpResponseRedirect('password_reset_done')
        return super().form_valid(form)
