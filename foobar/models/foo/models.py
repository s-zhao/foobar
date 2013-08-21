""" corporate directory        
[shichang-scz.rhcloud.com foobar]\> python manage-dev.py syncdb
CommandError: One or more models did not validate:
foo.person: Accessor for field 'contact' clashes with related field 'PersonalContact.person'. Add a related_name argument to the definition for 'contact'.
foo.person: Reverse query name for field 'contact' clashes with related field 'PersonalContact.person'. Add a related_name argument to the definition for 'contact'.


"""
"""

#
# organization contact directory
#
from django.db import models

class Address(models.Model):
    line1 = models.CharField(max_length=50, blank=False)
    line2 = models.CharField(max_length=50, blank=True, null=False)
    city = models.CharField(max_length=50, blank=False)
    state = models.CharField(max_length=2, blank=False)
    zip_code = models.CharField(max_length=32, blank=False)
    country = models.CharField(max_length=3, blank=False)
    
    def __unicode__(self):
        return u'%s, %s %s' % (self.line1, self.city, self.state)

class PersonalContact(Address):    
    home_phone = models.CharField(max_length=32, blank=True, null=False)
    work_phone = models.CharField(max_length=32, blank=True, null=False)
    mobile = models.CharField(max_length=32, blank=True, null=False)
    email = models.EmailField(blank=True, null=False) #max_length=75, 
    url = models.URLField(blank=True, null=False) #max_length=200

    notes = models.TextField(blank=True, null=False)

class BusinessContact(Address):
    phone = models.CharField(max_length=32, blank=True, null=False)
    email = models.EmailField(blank=True, null=False) #max_length=75, 
    url = models.URLField(blank=True, null=False) #max_length=200

    notes = models.TextField(blank=True, null=False)
    
#
# entity - in nature how we define a person
# data ownership - organization
#   therefore, a real person may have multiple records in the system
#
#   API edit not allowed 
# 
class Person(models.Model):
    GENDER = (
        ('', 'No Reply'),
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    )
    
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=30, blank=False)
    middle_name = models.CharField("middle and initials", max_length=30, blank=True, null=False)

    gender = models.CharField(max_length=1, choices=GENDER, blank=True, null=False)
    dob = models.DateField("birth date", blank=True, null=True)
    
    #
    # OneToOneField => ForeignKey(model, unique=True)
    # so if intention is, each one shall have its own record, then use OneToOne
    # if intention is, multiple may share the same, use ForeignKey
    #
    # each person shall provide and maintain one's own birth place record
    #
    birth_place = models.OneToOneField(Address, blank=True, null=True) 
    
    ssn = models.CharField(max_length=9, blank=True, null=False)
    
    #
    # up to date best contact information
    #
    contact = models.OneToOneField(PersonalContact, blank=True, null=True)    

    def __unicode__(self):
        return u"%s %s" % (self.first_name, self.last_name)

class Organization(models.Model):
    name = models.CharField(max_length=50, unique=True, blank=False)
    description = models.TextField(blank=True, null=False)
    
    #
    #legal/public
    #
    contact = models.OneToOneField(BusinessContact, blank=False)
    
    def __unicode__(self):
        return u'%s' % self.name

class OfficeType(models.Model):

    class Meta:
        unique_together = ('sym', 'organization')
        
    name = models.CharField(max_length=50, unique=True, blank=False, null=False)
    sym = models.CharField(max_length=32, unique=True, blank=False, null=False)
    description = models.TextField(blank=True, null=False)
    
    organization = models.ForeignKey(Organization, blank=False)
    
    def __unicode__(self):
        return u'%s - %s' % (self.sym, self.name)

class DepartmentType(models.Model):

    class Meta:
        unique_together = ('sym', 'organization')
        
    name = models.CharField(max_length=50, unique=True, blank=False, null=False)
    sym = models.CharField(max_length=32, unique=True, blank=False, null=False)
    description = models.TextField(blank=True, null=False)
    
    organization = models.ForeignKey(Organization, blank=False)
    
    def __unicode__(self):
        return u'%s - %s' % (self.sym, self.name)
        
#
# POST - per organization settings
#
class Position(models.Model):

    class Meta:
        unique_together = ('sym', 'organization')
        
    name = models.CharField(max_length=50, unique=True, blank=False, null=False)
    sym = models.CharField(max_length=32, unique=True, blank=False, null=False)
    description = models.TextField(blank=True, null=False)
    
    organization = models.ForeignKey(Organization, blank=False)
    
    def __unicode__(self):
        return u'%s - %s' % (self.sym, self.name)

class Level(models.Model):
    
    class Meta:
        unique_together = ('sym', 'position')
        
    name = models.CharField(max_length=50, unique=True, blank=False, null=False)
    sym = models.CharField(max_length=32, unique=True, blank=False, null=False)
    description = models.TextField(blank=True, null=False)
    
    position = models.ForeignKey(Position)
    
    def __unicode__(self):
        return u'%s - %s' % (self.sym, self.name)

class Title(models.Model):
    
    class Meta:
        unique_together = ('sym', 'position')
        
    name = models.CharField(max_length=50, unique=True, blank=False, null=False)
    sym = models.CharField(max_length=32, unique=True, blank=False, null=False)
    description = models.TextField(blank=True, null=False)
    
    position = models.ForeignKey(Position)
    
    def __unicode__(self):
        return u'%s - %s' % (self.sym, self.name)
        
#full-time, contract, consultant ...        
class EmploymentType(models.Model):
    
    class Meta:
        unique_together = ('sym', 'organization')
        
    name = models.CharField(max_length=50, unique=True, blank=False, null=False)
    sym = models.CharField(max_length=32, unique=True, blank=False, null=False)
    description = models.TextField(blank=True, null=False)
    
    organization = models.ForeignKey(Organization, blank=False)
    
    def __unicode__(self):
        return u'%s - %s' % (self.sym, self.name)
                
class Office(models.Model):

    class Meta:
        unique_together = ('name', 'organization')
        
    name = models.CharField(max_length=50, unique=True, blank=False, null=False)
    description = models.TextField(blank=True, null=False)
    
    organization = models.ForeignKey(Organization, blank=False, null=True)
    office_type = models.ForeignKey(OfficeType, blank=False)

    contact = models.OneToOneField(BusinessContact)    
    
    work_hours = models.CharField(max_length=250, blank=True, null=False)
    weekend_hours = models.CharField(max_length=250, blank=True, null=False)
    holiday_hours = models.CharField(max_length=250, blank=True, null=False)
    
    #
    # regional primary office or head quarter
    #
    is_primary = models.BooleanField(default=False)
        
    def __unicode__(self):
        return u'%s - %s' % (self.name, self.organization.name)
    
class Department(models.Model):

    class Meta:
        unique_together = ('name', 'office')
        
    name = models.CharField(max_length=50, unique=True, blank=False, null=False)
    description = models.TextField(blank=True, null=False)
    
    office = models.ForeignKey(Office, blank=False, null=True)
    
    department_type = models.ForeignKey(DepartmentType, blank=False)
    contact = models.OneToOneField(BusinessContact)    
        
    work_hours = models.CharField(max_length=250, blank=True, null=False)
    weekend_hours = models.CharField(max_length=250, blank=True, null=False)
    holiday_hours = models.CharField(max_length=250, blank=True, null=False)
            
    def __unicode__(self):
        return u'%s - %s' % (self.name, self.office.name)
        
class Worker(models.Model):

    class Meta:
        #
        # the same person may be associated with mutliple departments
        #
        unique_together = ('person', 'department')
        
    #
    # corporate owned 'Person' record
    #   access to person record requires: department | department.office | department.office.organization
    #   and function permission
    #
    person = models.ForeignKey(Person)
    
    #
    # contact information given to and shared by this employment
    #
    contact = models.OneToOneField(PersonalContact)
    
    department = models.ForeignKey(Department)    
    
    start_date = models.DateField(blank=True, null=True)
    conversion_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    
    position = models.ForeignKey(Position)
    title = models.ForeignKey(Title)
    level = models.ForeignKey(Level)
    employment = models.ForeignKey(EmploymentType)

"""    
    