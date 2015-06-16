from django.contrib.admin import ModelAdmin, site
from .models import *

reg=site.register

class PersonAdmin(ModelAdmin): pass
reg(Person, PersonAdmin)

class AddressAdmin(ModelAdmin): pass
reg(Address, AddressAdmin)

class InvitationAdmin(ModelAdmin): pass
reg(Invitation, InvitationAdmin)

class MealOptionAdmin(ModelAdmin): pass
reg(MealOption, MealOptionAdmin)

class MealAdmin(ModelAdmin): pass
reg(Meal, MealAdmin)

class TableAdmin(ModelAdmin): pass
reg(Table, TableAdmin)

class TablePositionAdmin(ModelAdmin): pass
reg(TablePosition, TablePositionAdmin)