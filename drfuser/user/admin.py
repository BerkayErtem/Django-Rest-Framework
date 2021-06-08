from django.contrib import admin
from .models import Form, User, Company, Subsidiary, Image, Form
# Register your models here.
admin.site.register(User)
admin.site.register(Company)
admin.site.register(Subsidiary)
admin.site.register(Image) 
admin.site.register(Form)