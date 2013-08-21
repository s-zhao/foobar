"""
drop table foo_address;
drop table foo_person;
drop table foo_servicecontact;

drop table foo_location;
drop table foo_organization;
drop table foo_organizationcontact;
drop table foo_organizationlocation;

.schema foo_address
.schema foo_person
.schema foo_servicecontact

.schema foo_location
.schema foo_organization
.schema foo_organizationcontact
.schema foo_organizationlocation
"""

import random

from foobar.models.foo import models

streets =[
    '2nd', 'Highland', '3rd', '1st', 'Forest', '4th', 'Jefferson', 
    'Park', 'Hickory', '5th', 'Wilson', 'Main', 'River', '6th', 
    'Meadow', 'Oak', 'Valley', '7th', 'Seventh', 'Smith', 'Pine', 
    'East', 'Maple', 'Chestnut', 'Cedar', '13th', '8th', 'Franklin', 
    'Elm', 'Adams', 'View', '14th', 'Washington', 'Spruce', 'Ninth', 
    'Laurel', 'Lake', 'Davis', 'Hill', 'Birch', 'Walnut', 'Williams', 
    '10th', 'Tenth', 'Lee', 'Spring', 'Dogwood', 'North', 'Green', 
    'Ridge', 'Poplar', 'Lincoln', 'Locust', 'Church', 'Woodland', 
    'Willow', 'Taylor', 'Mill', 'Ash', 'Sunset', 'Madison', 'Railroad', 
    '15th', '11th', 'Hillcrest', 'Jackson', 'Sycamore', 'Cherry', 
    'Broadway', 'West', 'Miller', 'South', 'Lakeview', 
    '12th', 'College', 'Center', 'Central'
]

def generateStreetName():
    max = len(streets)-1
    i = random.randint(0, max)
    j = random.randint(0, 1)
    
    kind = ['St', 'Ave']
    
    return '%s %s %s' % (random.randint(1, 100), streets[i], kind[j])
    
for i in range(100):
    print generateStreetName()
   


def load_location_records():
    count = models.Location.objects.count()
    if count == 3:
        print 'locations already loaded'
        return
        
    locations = ['New York', 'Pittsburgh', 'Los Angeles']
    
    for loc in locations:
        models.Location.objects.create(name=loc)
    
    for loc in models.Location.objects.all():
        print loc
       
def load_organization_records():
    pass
    
def run():
    load_location_records()
    
    #
    # two ways to insert records
    #
    models.Address.objects.create(line1='Roy St.', city='Pittsburgh', state='PA', country='USA')
    address = models.Address(line1='#2 Roy St.', city='Pittsburgh', state='PA', country='USA')
    address.save()
    #print address.id
    
    for address in models.Address.objects.all():
        print address
    
    #models.Address.objects.all().delete()
    