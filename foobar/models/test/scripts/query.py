#

"""
keep original models untouched such that when an application
needs additional specific care, a new proxy may be created.

export PATH=$OPENSHIFT_DATA_DIR/bin:$PATH

"""
import decimal, uuid

from django.db import models
from django.db.models import F, Q, Avg, Max, Min, Count, Sum

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
    
class MyRegistrationManager(models.Manager):
    def get_query_set(self):
        queryset = MyQuerySet(self.model)
        return queryset
        
class Registration(test.models.Registration):
    class Meta:
        proxy = True
    
    objects = MyRegistrationManager()     
    
    def __unicode__(self):
        return u'%s %s' % (self.date, self.car)

def test_basic():
    #
    # drill down
    #
    dodge = test.models.Maker.objects.get(name='DODGE')
    model = dodge.mdl_set.get(name='CARAVAN')
    car = model.car_set.get(year=2010)
    print 
    for r in car.registration_set.all().iterator():
        print r
    
    #
    # follow relation
    #
    qset = Registration.objects.filter(car__model__maker__name='DODGE', car__year=2010, car__model__name='CARAVAN')
    print
    for r in qset.all():
        print r
    
def test_F_Q():
    notPA = ~Q(state='PA')
    above_mrp = Q(price__gt = F('car__mrp'))
    
    PA = Q(state='PA')
    below_mrp = Q(price__lt = F('car__mrp'))
    
    qset = Registration.objects.filter( (notPA & above_mrp) | (PA & below_mrp) )
    
    #
    # show query 
    #
    print qset.query
    """
        SELECT "test_registration"."id", "test_registration"."date", "test_registration"."state", "test_registration"."zip", "test_registration"."reg_type_car", 
                "test_registration"."car_id", "test_registration"."price", "test_registration"."vin", "test_registration"."notes" 
                FROM "test_registration" INNER JOIN "test_car" ON ("test_registration"."car_id" = "test_car"."id") 
                WHERE (
                    (NOT ("test_registration"."state" = PA ) AND "test_registration"."price" >  "test_car"."mrp") 
                    OR 
                    ("test_registration"."state" = PA  AND "test_registration"."price" <  "test_car"."mrp")
                )
    """
    
    print 'count: ', qset.count()
    
def test_annotate():
    #
    # annotate - return queryset
    #
    qset = test.models.Maker.objects.annotate(num_of_models=Count('mdl'))
    print
    print 'total number of models'
    print qset.query
    for r in qset:
        print r.name, r.num_of_models
    
    #
    # list of objects - reverse relation - use lowcase of related model name
    #
    qset = test.models.Maker.objects.annotate(total_sold=Sum('mdl__car__registration__price'))    
    print
    print 'total sold'
    print qset.query
    for r in qset:
        print r.name, r.total_sold

    #
    # list of dict
    #
    qset = test.models.Maker.objects.annotate(total_sold=Sum('mdl__car__registration__price')).values('name', 'total_sold')
    print
    print 'total sold'
    print qset.query
    for r in qset:
        print r['name'], r['total_sold']
    
    #
    # use values() to limit fields and order_by to clear off extra fields in GROUP BY
    #
    qset = Registration.objects.filter(car__model__maker__name='DODGE').values('car__year').annotate(yearly_sales=Sum('price')).order_by()
    print
    print qset.query
    for r in qset:
        print r['car__year'], r['yearly_sales']
     
    #
    # with order by
    #
    qset = test.models.Car.objects.filter(model__maker__name='DODGE', year__gte=2010). \
        values('registration__state'). \
        annotate(sales=Sum('registration__price'), count=Count('registration__id'), avg_price=Avg('registration__price')). \
        order_by('-sales')
    print
    print qset.query
    print qset.count()
    for r in qset:
        print r
        
    
def test_aggregate():
    #
    # aggregate - return summary values
    #
    data = test.models.Car.objects.filter(model__maker__name='DODGE', year__gte=2010).aggregate(count=Count('registration__id'), total=Sum('registration__price'))
    print
    print data
    
    #
    # show query statements
    #
    from django.db.models import connection
    print
    print connection.queries
    
def test_raw():
    """
        so just use python DBI2
    """
    #
    #extra(select=None, where=None, params=None, tables=None, order_by=None, select_params=None)
    #
    
    # from django.db.models import connection
    # cursor = connection.cursor()
    # cursor.execute(sql, [params])
    # ... => python dbi ..
    #
    # from django.db.models import connections
    # connection = connections['the-db']
    # ...
    #    
    pass
    
    
def run():
    #test_basic()
    #test_F_Q()
    test_annotate()
    test_aggregate()
    
    
    