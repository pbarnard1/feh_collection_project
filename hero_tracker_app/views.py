from django.shortcuts import render, redirect
from .models import *
import bcrypt
from django.contrib import messages
from django.contrib.messages import get_messages
from datetime import datetime, date, timedelta, timezone

# Create your views here.
def index(request):
    if 'uid' in request.session: # If logged in already
        return redirect('/my_heroes') # Head straight to heroes page
    else:
        return redirect('/log_in_page') # Go to log-in page

def my_heroes(request):
    if 'uid' not in request.session: # If not logged in
        return redirect('/log_in_page') # Head to log-in page
    user_obj = User.objects.get(id=request.session['uid'])
    user_heroes = user_obj.heroes.all()
    all_heroes = Hero.objects.all()
    hero_data = []
    for hero in user_heroes:
        hero_data.append({
            'hero': hero.name,
            'movement': hero.movement_type,
            'weapon': hero.weapon_type,
            'color': hero.color,
            'debut_date': hero.debut_date,
            'hp': hero.lv_40_HP,
            'atk': hero.lv_40_atk,
            'spd': hero.lv_40_spd,
            'def': hero.lv_40_def,
            'res': hero.lv_40_res,
        })
    valDict = {
        'user_heroes': hero_data,
        'hero_objects': all_heroes,
        'user': user_obj,
    }
    return render(request, 'main_page.html', context=valDict)

def log_in_page(request):
    if 'uid' in request.session: # If logged in already
        return redirect('/my_heroes') # Head straight to heroes page
    else:
        all_messages = get_messages(request) # Get messages (or tags in this case)
        valDict = {}
        if all_messages: # If there is an error message
            valDict['tags'] = []
            for message in all_messages:
                valDict['tags'].append(message.extra_tags) # Either "is-valid" or "is-invalid"
            try:
                valDict['alias'] = request.session['alias']
            except:
                pass
        return render(request, 'login_page.html', context=valDict)

def log_in(request):
    if 'uid' in request.session: # If logged in already
        return redirect('/my_heroes') # Head straight to heroes page
    # see if the alias provided exists in the database
    user = User.objects.filter(alias=request.POST['alias']) # Filter used to ensure it runs if nobody is around (get could produce an error)
    request.session['alias'] = request.POST['alias']
    if user: # note that we take advantage of truthiness here: an empty list will return false
        logged_user = user[0]
        # assuming we only have one user with this username, the user would be first in the list we get back
        # of course, we should have some logic to prevent duplicates of usernames when we create users
        # use bcrypt's check_password_hash method, passing the hash from our database and the password from the form
        if bcrypt.checkpw(request.POST['pwd'].encode(), logged_user.pwd_hsh.encode()):
            # if we get True after checking the password, we may put the user id in session
            request.session['uid'] = logged_user.id
            # never render on a post, always redirect!
            return redirect('/my_heroes')
    # if we didn't find anything in the database by searching by username or if the passwords don't match, 
    # redirect back to a safe route
    messages.error(request, "Invalid e-mail and/or password", extra_tags="is-invalid")
    return redirect('/log_in_page')

def registration_page(request):
    if 'uid' in request.session: # If logged in already
        return redirect('/my_heroes') # Head straight to heroes page
    else: # Not logged in, so show log-in page
        all_messages = get_messages(request) # Get messages (or tags in this case)
        valDict = {}
        if all_messages: # If there is an entry
            valDict['tags'] = []
            for message in all_messages:
                valDict['tags'].append(message.extra_tags) # Either "is-valid" or "is-invalid"
            valDict['first_name'] = request.session['first_name']
            valDict['last_name'] = request.session['last_name']
            valDict['alias'] = request.session['alias']
            valDict['email'] = request.session['email']
            del request.session['first_name']
            del request.session['last_name']
            del request.session['email']
        return render(request,'registration_page.html',context=valDict)

def register(request):
    if 'uid' in request.session: # If logged in already
        return redirect('/my_heroes') # Head straight to heroes page
    # Validate everything first to make sure it's valid
    errorDict, isValidDict = User.objects.validate_data(request.POST,User.objects.all())
    if list(isValidDict.values()).count('is-invalid') > 0: # If there's an error, go back
        for value in isValidDict.values():
            messages.error(request, value, extra_tags=value)
        request.session['first_name'] = request.POST['first_name']
        request.session['last_name'] = request.POST['last_name']
        request.session['alias'] = request.POST['alias']
        request.session['email'] = request.POST['email']
        return redirect('/registration_page')
    else: # Successful creation of account
        # include some logic to validate user input before adding them to the database!
        password = request.POST['pwd']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()  # create the hash    
        # be sure you set up your database so it can store password hashes this long (60 characters)
        # make sure you put the hashed password in the database, not the one from the form!
        new_user = User.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'], \
            alias= request.POST['alias'], email = request.POST['email'], pwd_hsh = pw_hash)
        # messages.success(request,'Account created successfully')
        request.session['uid'] = new_user.id
        # Give new user default heroes: Alfonse, Sharena and Anna
        alfonse_obj = Hero.objects.get(name="Alfonse",id=1)
        sharena_obj = Hero.objects.get(name="Sharena",id=2)
        anna_obj = Hero.objects.get(name="Anna",id=3)
        new_user.heroes.add(alfonse_obj,sharena_obj,anna_obj)
        return redirect('/my_heroes') # never render on a post, always redirect! 

def log_out(request):
    request.session.clear() # Delete session since user is logged out
    messages.success(request,'You have logged out successfully', extra_tags="logged_out")
    return redirect('/')

def view_stats(request):
    if 'uid' not in request.session: # If not logged in already
        return redirect('/log_in_page') # Head to log-in page
    else:
        user_obj = User.objects.get(id=request.session['uid'])
        valDict = {
            'user': user_obj,
        }
        return render(request,'my_stats.html',context=valDict)

def all_heroes(request):
    if 'uid' not in request.session: # If not logged in already
        return redirect('/log_in_page') # Head to log-in page
    else:
        all_heroes = Hero.objects.all()
        hero_data = []
        for hero in all_heroes:
            hero_data.append({
                'hero': hero.name,
                'movement': hero.movement_type,
                'weapon': hero.weapon_type,
                'color': hero.color,
                'debut_date': hero.debut_date,
                'hp': hero.lv_40_HP,
                'atk': hero.lv_40_atk,
                'spd': hero.lv_40_spd,
                'def': hero.lv_40_def,
                'res': hero.lv_40_res,
            })
        valDict = {
            'all_heroes': hero_data,
        }
        return render(request,'all_heroes.html',context=valDict)

# Make database from scratch - ONLY RUN ONCE!!!
def new_database(request):
    # Generate the list of heroes
    # Hero.objects.create(name="Alfonse",desc="Prince of Askr",movement_type="Infantry",weapon_type="Sword", \
    #     color="Red",debut_date="2017-02-02",lv_40_HP=43,lv_40_atk=35,lv_40_spd=25,lv_40_def=32,lv_40_res=22)
    # Hero.objects.create(name="Sharena",desc="Princess of Askr",movement_type="Infantry",weapon_type="Lance", \
    #     color="Blue",debut_date="2017-02-02",lv_40_HP=43,lv_40_atk=32,lv_40_spd=32,lv_40_def=29,lv_40_res=22)
    # Hero.objects.create(name="Anna",desc="Commander of Askr",movement_type="Infantry",weapon_type="Axe", \
    #     color="Green",debut_date="2017-02-02",lv_40_HP=41,lv_40_atk=29,lv_40_spd=38,lv_40_def=22,lv_40_res=28)
    # Hero.objects.create(name="Takumi",desc="Younger prince of Hoshido",movement_type="Infantry",weapon_type="Bow", \
    #     color="Colorless",debut_date="2017-02-02",lv_40_HP=40,lv_40_atk=32,lv_40_spd=33,lv_40_def=25,lv_40_res=18)
    # Hero.objects.create(name="Ryoma",desc="Older prince of Hoshido",movement_type="Infantry",weapon_type="Sword", \
    #     color="Red",debut_date="2017-02-02",lv_40_HP=41,lv_40_atk=34,lv_40_spd=35,lv_40_def=27,lv_40_res=21)
    # Hero.objects.create(name="Sanaki",desc="Empress of the empire of Begnion",movement_type="Infantry",weapon_type="Tome", \
    #     color="Red",debut_date="2017-02-27",lv_40_HP=33,lv_40_atk=37,lv_40_spd=26,lv_40_def=17,lv_40_res=34)
    # Hero.objects.create(name="Linde",desc="Archanean light mage",movement_type="Infantry",weapon_type="Tome", \
    #     color="Blue",debut_date="2017-02-02",lv_40_HP=35,lv_40_atk=35,lv_40_spd=36,lv_40_def=14,lv_40_res=27)
    # Hero.objects.create(name="Lissa",desc="Younger princess of Ylisse",movement_type="Infantry",weapon_type="Staff", \
    #     color="Colorless",debut_date="2017-02-02",lv_40_HP=39,lv_40_atk=26,lv_40_spd=25,lv_40_def=28,lv_40_res=30)
    
    # Generate list of skills
    return redirect('/')