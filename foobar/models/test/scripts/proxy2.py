"""
keep original models untouched such that when an application
needs additional specific care, a new proxy may be created.

export PATH=$OPENSHIFT_DATA_DIR/bin:$PATH

"""
import decimal

from django.db import models
from django.db.models import F, Q

from django.db.models.query import QuerySet

from foobar.models import test

#
# queryset provided custom query filters
#
class MyQuerySet(QuerySet):
    def dodge2012(self):
        return self.filter(car__year=2012, car__model__maker__name='DODGE')
    
    def below_mrp(self):
        return self.filter(price__lt = F('car__mrp'))
    
    #
    # bulk delete, update
    #
    
class MyRegistrationManager(models.Manager):
    def get_query_set(self):
        """
        this manager's default queryset

        use cases:
        
            - implicity: manager.filter(...) 
            - explicity: manager.get_query_set().filter(...)        
        """
        return MyQuerySet(self.model)
        
        
class Registration(test.models.Registration):
    class Meta:
        proxy = True
    
    qmgr = MyRegistrationManager()
    
    #
    # override default manager
    #
    objects = qmgr     
            
    def __unicode__(self):
        return u'%s: %s %s' % (self.__class__, self.car.year, self.car.model.name)
        
        
def query():
    
    qset = Registration.objects.get_query_set().dodge2012().filter(state='PA')
    print
    print qset.__class__
    print "dodge 2012 PA count: ", qset.count()
    
    #
    # another way
    #
    qset = Registration.objects.filter(state='PA').dodge2012()
    print "dodge 2012 PA count: ", qset.count()
    
    print "dodge 2012 PA below mrp count: ", qset.below_mrp().count()
    
    #
    # note .all() returns a queryset, not db records!
    #
    first_registration = qset.all()[1] # new in 1.6: qset.first(), last()
    print
    print first_registration
    
def run():
    query()
    
    
    