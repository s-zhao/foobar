#
from django.contrib import admin

from foobar.models.test.models import Klass, Maker, Mdl, Car, Registration

#class PollAdmin(admin.ModelAdmin):
#    fields = ['pub_date', 'question']
#admin.site.register(Poll, PollAdmin)

admin.site.register(Klass)
admin.site.register(Maker)
admin.site.register(Mdl)
admin.site.register(Car)
admin.site.register(Registration)
