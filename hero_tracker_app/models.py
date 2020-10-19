from django.db import models
from datetime import date, datetime # For comparing dates
import re # For regular expression support (e.g. e-mails)

# Model validations go here.
class UserValidator(models.Manager):
    def validate_data(self, post_data, user_list):
        errorDict = {} # Empty dictionary containing errors
        isValidDict = {}
        # Now check each field here.
        if len(post_data['first_name']) < 2 or len(post_data['first_name']) > 255:
            errorDict['first_name'] = 'First name must be 2-255 characters long.'
            isValidDict['first_name_valid'] = "is-invalid"
        elif not post_data['first_name'].isalpha():
            errorDict['first_name'] = 'Name must only contain letters'
            isValidDict['first_name_valid'] = "is-invalid"
        else:
            isValidDict['first_name_valid'] = "is-valid"
        if len(post_data['last_name']) < 2 or len(post_data['last_name']) > 255:
            errorDict['last_name'] = 'Last name must be 2-255 characters long.'
            isValidDict['last_name_valid'] = "is-invalid"
        elif not post_data['last_name'].isalpha():
            errorDict['last_name'] = 'Name must only contain letters.'
            isValidDict['last_name_valid'] = "is-invalid"
        else:
            isValidDict['last_name_valid'] = "is-valid"
        if len(post_data['alias']) < 2 or len(post_data['alias']) > 255:
            errorDict['alias'] = 'Alias must be 2-255 characters long.'
            isValidDict['alias_valid'] = "is-invalid"
        else:
            dupe_aliases = user_list.filter(alias=post_data['alias'])
            if dupe_aliases: # If e-mail already found 
                errorDict['alias'] = 'Another person already registered with this alias.'
                isValidDict['alias_valid'] = "is-invalid"
            else:
                isValidDict['alias_valid'] = "is-valid"
        # Process invalid e-mails here (from Coding Dojo)
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(post_data['email']):    # test whether a field matches the pattern            
            errorDict['email'] = "E-mail address is invalid."
            isValidDict['email_valid'] = "is-invalid"
        # Look through all e-mails in database to make sure there's no duplicate
        else: # Now check to see if someone with that e-mail is already registered
            dupe_emails = user_list.filter(email=post_data['email'])
            if dupe_emails: # If e-mail already found 
                errorDict['email'] = 'Another person already registered with this e-mail.'
                isValidDict['email_valid'] = "is-invalid"
            else:
                isValidDict['email_valid'] = "is-valid"
        if post_data['pwd'] != post_data['pwd2']:
            errorDict['pwd'] = 'Passwords must agree.'
            isValidDict['pwd_valid'] = "is-invalid"
        elif len(post_data['pwd']) < 8:
            errorDict['pwd'] = 'Password must be 8 or more characters long.'
            isValidDict['pwd_valid'] = "is-invalid"
        else:
            isValidDict['pwd_valid'] = "is-valid"
        return errorDict, isValidDict

# class BookValidator(models.Manager):
#     def validate_data(self, post_data):
#         errorDict = {}
#         if len(post_data['title']) < 2 or len(post_data['first_name']) > 255:
#             errorDict['title'] = 'Title must be 2-255 characters long'
#         return errorDict

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.EmailField()
    pwd_hsh = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    objects = UserValidator()
    # heroes # TEMPORARY

    def __str__(self):
        return f"User named {self.first_name} {self.last_name}"

class Hero(models.Model):
    name = models.CharField(max_length=255) # Name of hero
    # epithet = models.CharField(max_length=255) # Example: Princess of Askr for Sharena
    desc = models.TextField() # Description about hero
    # games = many-to-many field # Games in the series the hero appears in other than Fire Emblem Heroes
    # skills = one-to-many field # Each hero can have many skills; one-to-many since some haven't learned it while others have
    movement_type = models.CharField(max_length=255) # Infantry, cavalry, flier or armor
    weapon_type = models.CharField(max_length=255) # Sword, axe, lance, beast, tome, bow, staff, dagger
    color = models.CharField(max_length=255) # Color: red, blue, green or colorless
    debut_date = models.DateField() # Date hero debuted in game
    # debuted_in = models.CharField(max_length=255) # Name of debut banner - or GHB/TT unit
    # book_number = models.IntegerField() # Book number
    # # Is summonable in certain pools
    # is_in_3_star_pool = models.BooleanField(default=True)
    # is_in_4_star_pool = models.BooleanField(default=True)
    # is_in_5_star_pool = models.BooleanField(default=False)
    # # Is a special type of hero
    # is_legendary_hero = models.BooleanField(default=False)
    # is_mythic_hero = models.BooleanField(default=False)
    # is_duo_hero = models.BooleanField(default=False)

    # blessing = models.CharField(max_length=255,default=None)
    
    # TEMPORARY
    users = models.ManyToManyField('User',related_name="heroes")

    # # Level 1 stats (will vary by rarity)
    # lv_1_HP = models.IntegerField()
    # lv_1_atk = models.IntegerField()
    # lv_1_spd = models.IntegerField()
    # lv_1_def = models.IntegerField()
    # lv_1_res = models.IntegerField()
    # Level 40 stats
    lv_40_HP = models.IntegerField()
    lv_40_atk = models.IntegerField()
    lv_40_spd = models.IntegerField()
    lv_40_def = models.IntegerField()
    lv_40_res = models.IntegerField()
    # Level 40 superboons and superbanes (will vary by rarity)

    # Voice actors and actresses
    # Image links
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    # objects = HeroValidator()

    def __str__(self):
        return f"Hero named {self.name}"

# class Game(models.Model):
#     title = models.CharField(max_length=255)
#     release_date_JP = models.DateField()
#     heroes = models.ManyToManyField('Hero',related_name="games")
#     created_on = models.DateTimeField(auto_now_add=True)
#     updated_on = models.DateTimeField(auto_now=True)

# class Hero_Stat(models.Model):
#     pass

# class Skill(models.Model):
#     name = models.CharField(max_length=255) # Weapon, support skill, special, A skill, B skill, C skill
#     desc = models.TextField() # Text description about skill
#     hero = models.ForeignKey('Hero',related_name="skills",on_delete=models.CASCADE)
#     # weapon_types <-- One-to-many field to see which weapon types can use that skill
#     # movement_types <-- One-to-many field to see which movement types can use that skill 
#     is_learned = models.BooleanField(default=False) # Whether hero comes with skill learned
#     created_on = models.DateTimeField(auto_now_add=True)
#     updated_on = models.DateTimeField(auto_now=True)

# class WeaponType(models.Model):
#     weapon_type = models.CharField(max_length=255)
#     skill = models.ForeignKey('Skill',related_name="weapon_types",on_delete=models.CASCADE)
#     created_on = models.DateTimeField(auto_now_add=True)
#     updated_on = models.DateTimeField(auto_now=True)

# class MovementType(models.Model):
#     movement_type = models.CharField(max_length=255)
#     skill = models.ForeignKey('Skill',related_name="movement_types",on_delete=models.CASCADE)
#     created_on = models.DateTimeField(auto_now_add=True)
#     updated_on = models.DateTimeField(auto_now=True)