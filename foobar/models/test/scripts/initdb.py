#
import os, re, pprint, random, uuid, datetime, decimal

from foobar.models.test.models import Klass, Maker, Mdl, Car, Registration

def load_data_class():
    Klass.objects.all().delete()

    classes = ('Luxury', 'Family', 'Economy')
    for kls in classes:
        Klass.objects.create(name=kls)
    
    assert Klass.objects.count() == 3
    
def do_DTL():
    font = """<font face="Arial" size="1">"""
    cols = re.compile(r'>(?P<value>.*?)</td>')
    
    is_year = year = re.compile(r'\d{4}')
    
    d = os.path.split(os.path.abspath(__file__))[0]
    doc = open(os.path.join(d, 'catalog.htm'), 'rb').read()
    doc = doc.strip().replace(' '*2, ' ').replace(font, '').replace('</font>', '')
    
    rows = doc.split('</tr><tr>')
    
    data = []
    catalog = {}
    
    for row in rows:
        values = cols.findall(row)
        if len(values) < 4: 
            continue;
            
        maker = values[1].strip()
        model = values[2].strip()
        year = values[3].strip()
        
        if not maker or not model or not is_year.match(year):
            continue
            
        if not catalog.get(maker):
            catalog[maker] = []
        if model not in catalog[maker]:
            catalog[maker].append(model)
            
        data.append( [maker, model, year] )
        
    if 0:
        out = pprint.pformat(data)
        open(os.path.join(d, 'out'), 'wb').write(
            pprint.pformat(catalog) + "\n\n" + 
            pprint.pformat(data)
        )
        
    Maker.objects.all().delete()
    Mdl.objects.all().delete()
    
    classes = ('Luxury', 'Family', 'Economy')
    
    _makers = ['DODGE', 'HONDA', 'NISSAN', 'JEEP',
                'HYUNDAI', 'TOYOTA']

    
    for maker, models in catalog.items():
        if maker not in _makers:
            continue
            
        maker = Maker.objects.create(name=maker)
            
        for model in models:
            klass = classes[random.randint(0, 2)]
            klass = Klass.objects.get(name=klass)
            
            d = {'name': model, 'klass': klass, 'maker': maker, 'year_begin': 1990+random.randint(1,10)}
            
            endyear = random.randint(1,100)+2005
            if endyear < 2013:
                d['year_end'] = endyear
                
            Mdl.objects.create(**d)
                
    print "total car models created: ", Mdl.objects.count()
    
def load_car():
    class_price = { #MRP
        'Luxury': (20, 25, 30, 35, 40, 45, 60, 65, 100),
        'Family': (12, 15, 20, 25, 35),
        'Economy': (10, 12, 14, 16, 18, 20, 26, 30)
    }
    classes = class_price.keys()
    
    Car.objects.all().delete()
    
    for mdl in Mdl.objects.all().iterator():
        year_end = (mdl.year_end or 2013)+1
        klass = mdl.klass.name
        
        for year in range(mdl.year_begin, year_end):
            mrp = class_price[klass][random.randint(0, len(class_price[klass])-1)]
            car = {'year': year, 'mrp': mrp*1000}
            mdl.car_set.add(Car(**car))
            
    print "total cars: ", Car.objects.count()
    
def load_registration():
    state_zip = {
        'NY': (10001, 14975),
        'PA': (15001, 19640), 
        'OH': (43001, 45999), 
        'FL': (32004, 34997),
        'DC': (20001, 20799)
    }
    states = state_zip.keys()    
        
    for car in Car.objects.all().iterator():
        for i in range(0, random.randint(1, 10)):
            month = random.randint(1, 12)
            day = random.randint(1, 28)
            date = datetime.date(car.year, month, day)
            
            #
            # money related calculation, can be complicated
            #
            factor = ['0.95', '1.0', '1.05'][random.randint(0,2)]
            price = decimal.Decimal(factor)*car.mrp
                    
            vin = uuid.uuid4().hex.upper()
            
            r = {'car': car, 'vin': vin, 'date': date, 'price': price, 'reg_type_car': Registration.NEW_CAR}
        
            state = states[random.randint(0, len(states)-1)]
            zip_range = state_zip[state]
            
            zip = random.randint(*zip_range)
            
            r['state'] = state
            r['zip']= zip
            
            Registration.objects.create(**r)
        
def run():
    #for maker in Maker.objects.all():
    ##    print maker
    #return
    
    if Klass.objects.count() == 0:
        load_data_class()
    
    if Mdl.objects.count() == 0:
        do_DTL()
    
    #stopped = Mdl.objects.filter(year_end__isnull=False)
    #print stopped.count()
    
    if Car.objects.count() == 0:
        load_car()
    
    if 1 or Registration.objects.count() == 0:
        load_registration()
    
