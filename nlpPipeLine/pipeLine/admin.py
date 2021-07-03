from django.contrib import admin

from .models import User, Pipeline, Pipe, Function#, Rule

admin.site.register(User)
admin.site.register(Pipeline)
admin.site.register(Pipe)
admin.site.register(Function)
#admin.site.register(Rule)
