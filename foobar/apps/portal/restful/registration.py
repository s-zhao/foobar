from tastypie.authorization import Authorization
from tastypie.resources import ModelResource

from foobar.models.test.models import Maker


class MakerResource(ModelResource):
    class Meta:
        queryset = Maker.objects.all()
        resource_name = 'maker'
        authorization= Authorization()
