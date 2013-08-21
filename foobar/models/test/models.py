"""django examples
    export PATH=$OPENSHIFT_DATA_DIR/bin:$PATH    
"""

from django.db import models
#http://www-nrd.nhtsa.dot.gov/database/aspx/vehdb/veh_catalog_by_mmy.aspx
#http://en.wikipedia.org/wiki/Car_classification

    
class Klass(models.Model):
    name = models.CharField(max_length=30, unique=True, blank=False)
    description = models.TextField(blank=True, null=False)
    
    def __unicode__(self):
        return u'%s' % self.name

class Maker(models.Model):
    name = models.CharField(max_length=30, unique=True, blank=False)
    description = models.TextField(blank=True, null=False)
    
    def __unicode__(self):
        return u'%s' % self.name
        
class Mdl(models.Model):
    class Meta:
        unique_together = ('name', 'maker')
        
    name = models.CharField(max_length=30, blank=False)    
    description = models.TextField(blank=True, null=False)

    klass = models.ForeignKey(Klass)    
    maker = models.ForeignKey(Maker)
    
    year_begin = models.IntegerField(default=0)
    year_end = models.IntegerField(blank=True, null=True)
        
    def __unicode__(self):
        return u'%s' % self.name
        
class Car(models.Model):
    year = models.IntegerField(default=0, blank=False)
    model = models.ForeignKey(Mdl)
    mrp = models.DecimalField(max_digits=19, decimal_places=2, default=0.00)
    
    description = models.TextField(blank=True, null=False, default="")
    url = models.URLField(blank=True, null=False)
    
    def __unicode__(self):
        return u'%s > %s > %s' % (self.model.maker.name, self.year, self.model.name)
        
class Registration(models.Model):
    USED_CAR = "USED"
    NEW_CAR = "NEW"    
    OTHER = "OTHER"
    
    REG_TYPE_CAR_CHOICES = (
        (NEW_CAR, 'Brand New'),
        (USED_CAR, 'Used'),
        (OTHER, 'Other')
    )
    
    #reg_person =
    date = models.DateField(blank=False)
    state = models.CharField(max_length=2, blank=False)
    zip = models.CharField(max_length=5, blank=True, null=False)
    
    reg_type_car = models.CharField(max_length=32, choices=REG_TYPE_CAR_CHOICES, default=OTHER)
    
    car = models.ForeignKey(Car)
    price = models.DecimalField(max_digits=19, decimal_places=2, default=0)
    vin = models.CharField(max_length=32, blank=False)
    
    notes = models.TextField(blank=True, null=False, default="")
    
    def __unicode__(self):
        return u'%s %s' % (self.date, self.car)
    
