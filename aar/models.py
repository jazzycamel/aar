from itertools import groupby
import os, random, string
from qrcode import *

from django.db.models import *
from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator

class Person(Model):
    TITLE_CHOICES=("Ms", "Miss", "Mrs", "Mr", "Master", "Dr")

    title=CharField(
        max_length=6,
        choices=tuple((c,c) for c in TITLE_CHOICES),
        blank=False,
        null=False
    )
    firstName=CharField("First Name", max_length=80, blank=False, null=False)
    lastName=CharField("Last Name", max_length=80, blank=False, null=False)
    email=EmailField(blank=True, null=True)

    phone_regex=RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone=CharField(
        max_length=15,
        blank=True,
        null=True,
        validators=[phone_regex]
    )

    address=ForeignKey('Address', related_name="person", blank=True, null=True, on_delete=SET_NULL)
    invitation=ForeignKey('Invitation', related_name="person", blank=True, null=True, on_delete=SET_NULL)

    attendingDay=BooleanField(default=False)
    attendingNight=BooleanField(default=False)

    weddingParty=BooleanField(default=False)
    child=BooleanField(default=False)

    meal=OneToOneField('Meal', related_name='person', blank=True, null=True, on_delete=SET_NULL)
    tablePosition=OneToOneField('TablePosition', related_name='person', blank=True, null=True, on_delete=SET_NULL)

    def __repr__(self): return "{0} {1}".format(self.firstName, self.lastName)
    def __str__(self): return repr(self)

class Address(Model):
    address1=CharField("Address Line 1", max_length=80, blank=True, null=True)
    address2=CharField("Address Line 2", max_length=80, blank=True, null=True)
    address3=CharField("Address Line 3", max_length=80, blank=True, null=True)
    address4=CharField("Address Line 4", max_length=80, blank=True, null=True)
    address5=CharField("Address Line 5", max_length=80, blank=True, null=True)
    townCity=CharField("Town/City", max_length=80, blank=True, null=True)

    COUNTY_CHOICES=(
        ('England',
            (
                ("Avon",)*2,
                ("Bedfordshire",)*2,
                ("Berkshire",)*2,
                ("Buckinghamshire",)*2,
                ("Cambridgeshire",)*2,
                ("Cheshire",)*2,
                ("Cleveland",)*2,
                ("Cornwall",)*2,
                ("Cumbria",)*2,
                ("Derbyshire",)*2,
                ("Devon",)*2,
                ("Dorset",)*2,
                ("Durham",)*2,
                ("East Sussex",)*2,
                ("Essex",)*2,
                ("Gloucestershire",)*2,
                ("Hampshire",)*2,
                ("Herefordshire",)*2,
                ("Hertfordshire",)*2,
                ("Isle of Wight",)*2,
                ("Kent",)*2,
                ("Lancashire",)*2,
                ("Leicestershire",)*2,
                ("Lincolnshire",)*2,
                ("London",)*2,
                ("Merseyside",)*2,
                ("Middlesex",)*2,
                ("Norfolk",)*2,
                ("Northamptonshire",)*2,
                ("Northumberland",)*2,
                ("North Humberside",)*2,
                ("North Yorkshire",)*2,
                ("Nottinghamshire",)*2,
                ("Oxfordshire",)*2,
                ("Rutland",)*2,
                ("Shropshire",)*2,
                ("Somerset",)*2,
                ("South Humberside",)*2,
                ("South Yorkshire",)*2,
                ("Staffordshire",)*2,
                ("Suffolk",)*2,
                ("Surrey",)*2,
                ("Tyne and Wear",)*2,
                ("Warwickshire",)*2,
                ("West Midlands",)*2,
                ("West Sussex",)*2,
                ("West Yorkshire",)*2,
                ("Wiltshire",)*2,
                ("Worcestershire",)*2,
            )
        ),
        ('Wales',
            (
                ("Clwyd",)*2,
                ("Dyfed",)*2,
                ("Gwent",)*2,
                ("Gwynedd",)*2,
                ("Mid Glamorgan",)*2,
                ("Powys",)*2,
                ("South Glamorgan",)*2,
                ("West Glamorgan",)*2,
            )
        ),
        ('Scotland',
            (
                ("Aberdeenshire",)*2,
                ("Angus",)*2,
                ("Argyll",)*2,
                ("Ayrshire",)*2,
                ("Banffshire",)*2,
                ("Berwickshire",)*2,
                ("Bute",)*2,
                ("Caithness",)*2,
                ("Clackmannanshire",)*2,
                ("Dumfriesshire",)*2,
                ("Dunbartonshire",)*2,
                ("East Lothian",)*2,
                ("Fife",)*2,
                ("Inverness-shire",)*2,
                ("Kincardineshire",)*2,
                ("Kinross-shire",)*2,
                ("Kirkcudbrightshire",)*2,
                ("Lanarkshire",)*2,
                ("Midlothian",)*2,
                ("Moray",)*2,
                ("Nairnshire",)*2,
                ("Orkney",)*2,
                ("Peeblesshire",)*2,
                ("Perthshire",)*2,
                ("Renfrewshire",)*2,
                ("Ross-shire",)*2,
                ("Roxburghshire",)*2,
                ("Selkirkshire",)*2,
                ("Shetland",)*2,
                ("Stirlingshire",)*2,
                ("Sutherland",)*2,
                ("West Lothian",)*2,
                ("Wigtownshire",)*2,
            )
        ),
        ('Northern Ireland',
            (
                ("Antrim",)*2,
                ("Armagh",)*2,
                ("Down",)*2,
                ("Fermanagh",)*2,
                ("Londonderry",)*2,
                ("Tyrone",)*2,
            )
        ),
    )
    county=CharField(max_length=20, choices=COUNTY_CHOICES, blank=True, null=True)

    postcode_regex=RegexValidator(
        regex=r'(\b[A-Z]{1,2}[0-9][A-Z0-9]? [0-9][ABD-HJLNP-UW-Z]{2}\b)',
        message=''
    )
    postCode=CharField(
        "Post Code",
        max_length=8,
        blank=True,
        null=True,
        validators=[postcode_regex]
    )

    COUNTRY_CHOICES=(
        ("Afghanistan",)*2,
        ("Albania",)*2,
        ("Algeria",)*2,
        ("Andorra",)*2,
        ("Angola",)*2,
        ("Antigua & Deps",)*2,
        ("Argentina",)*2,
        ("Armenia",)*2,
        ("Australia",)*2,
        ("Austria",)*2,
        ("Azerbaijan",)*2,
        ("Bahamas",)*2,
        ("Bahrain",)*2,
        ("Bangladesh",)*2,
        ("Barbados",)*2,
        ("Belarus",)*2,
        ("Belgium",)*2,
        ("Belize",)*2,
        ("Benin",)*2,
        ("Bhutan",)*2,
        ("Bolivia",)*2,
        ("Bosnia Herzegovina",)*2,
        ("Botswana",)*2,
        ("Brazil",)*2,
        ("Brunei",)*2,
        ("Bulgaria",)*2,
        ("Burkina",)*2,
        ("Burundi",)*2,
        ("Cambodia",)*2,
        ("Cameroon",)*2,
        ("Canada",)*2,
        ("Cape Verde",)*2,
        ("Central African Rep",)*2,
        ("Chad",)*2,
        ("Chile",)*2,
        ("China",)*2,
        ("Colombia",)*2,
        ("Comoros",)*2,
        ("Congo",)*2,
        ("Congo {Democratic Rep}",)*2,
        ("Costa Rica",)*2,
        ("Croatia",)*2,
        ("Cuba",)*2,
        ("Cyprus",)*2,
        ("Czech Republic",)*2,
        ("Denmark",)*2,
        ("Djibouti",)*2,
        ("Dominica",)*2,
        ("Dominican Republic",)*2,
        ("East Timor",)*2,
        ("Ecuador",)*2,
        ("Egypt",)*2,
        ("El Salvador",)*2,
        ("Equatorial Guinea",)*2,
        ("Eritrea",)*2,
        ("Estonia",)*2,
        ("Ethiopia",)*2,
        ("Fiji",)*2,
        ("Finland",)*2,
        ("France",)*2,
        ("Gabon",)*2,
        ("Gambia",)*2,
        ("Georgia",)*2,
        ("Germany",)*2,
        ("Ghana",)*2,
        ("Greece",)*2,
        ("Grenada",)*2,
        ("Guatemala",)*2,
        ("Guinea",)*2,
        ("Guinea-Bissau",)*2,
        ("Guyana",)*2,
        ("Haiti",)*2,
        ("Honduras",)*2,
        ("Hungary",)*2,
        ("Iceland",)*2,
        ("India",)*2,
        ("Indonesia",)*2,
        ("Iran",)*2,
        ("Iraq",)*2,
        ("Ireland {Republic}",)*2,
        ("Israel",)*2,
        ("Italy",)*2,
        ("Ivory Coast",)*2,
        ("Jamaica",)*2,
        ("Japan",)*2,
        ("Jordan",)*2,
        ("Kazakhstan",)*2,
        ("Kenya",)*2,
        ("Kiribati",)*2,
        ("Korea North",)*2,
        ("Korea South",)*2,
        ("Kosovo",)*2,
        ("Kuwait",)*2,
        ("Kyrgyzstan",)*2,
        ("Laos",)*2,
        ("Latvia",)*2,
        ("Lebanon",)*2,
        ("Lesotho",)*2,
        ("Liberia",)*2,
        ("Libya",)*2,
        ("Liechtenstein",)*2,
        ("Lithuania",)*2,
        ("Luxembourg",)*2,
        ("Macedonia",)*2,
        ("Madagascar",)*2,
        ("Malawi",)*2,
        ("Malaysia",)*2,
        ("Maldives",)*2,
        ("Mali",)*2,
        ("Malta",)*2,
        ("Marshall Islands",)*2,
        ("Mauritania",)*2,
        ("Mauritius",)*2,
        ("Mexico",)*2,
        ("Micronesia",)*2,
        ("Moldova",)*2,
        ("Monaco",)*2,
        ("Mongolia",)*2,
        ("Montenegro",)*2,
        ("Morocco",)*2,
        ("Mozambique",)*2,
        ("Myanmar, {Burma}",)*2,
        ("Namibia",)*2,
        ("Nauru",)*2,
        ("Nepal",)*2,
        ("Netherlands",)*2,
        ("New Zealand",)*2,
        ("Nicaragua",)*2,
        ("Niger",)*2,
        ("Nigeria",)*2,
        ("Norway",)*2,
        ("Oman",)*2,
        ("Pakistan",)*2,
        ("Palau",)*2,
        ("Panama",)*2,
        ("Papua New Guinea",)*2,
        ("Paraguay",)*2,
        ("Peru",)*2,
        ("Philippines",)*2,
        ("Poland",)*2,
        ("Portugal",)*2,
        ("Qatar",)*2,
        ("Romania",)*2,
        ("Russian Federation",)*2,
        ("Rwanda",)*2,
        ("St Kitts & Nevis",)*2,
        ("St Lucia",)*2,
        ("Saint Vincent & the Grenadines",)*2,
        ("Samoa",)*2,
        ("San Marino",)*2,
        ("Sao Tome & Principe",)*2,
        ("Saudi Arabia",)*2,
        ("Senegal",)*2,
        ("Serbia",)*2,
        ("Seychelles",)*2,
        ("Sierra Leone",)*2,
        ("Singapore",)*2,
        ("Slovakia",)*2,
        ("Slovenia",)*2,
        ("Solomon Islands",)*2,
        ("Somalia",)*2,
        ("South Africa",)*2,
        ("South Sudan",)*2,
        ("Spain",)*2,
        ("Sri Lanka",)*2,
        ("Sudan",)*2,
        ("Suriname",)*2,
        ("Swaziland",)*2,
        ("Sweden",)*2,
        ("Switzerland",)*2,
        ("Syria",)*2,
        ("Taiwan",)*2,
        ("Tajikistan",)*2,
        ("Tanzania",)*2,
        ("Thailand",)*2,
        ("Togo",)*2,
        ("Tonga",)*2,
        ("Trinidad & Tobago",)*2,
        ("Tunisia",)*2,
        ("Turkey",)*2,
        ("Turkmenistan",)*2,
        ("Tuvalu",)*2,
        ("Uganda",)*2,
        ("Ukraine",)*2,
        ("United Arab Emirates",)*2,
        ("United Kingdom",)*2,
        ("United States",)*2,
        ("Uruguay",)*2,
        ("Uzbekistan",)*2,
        ("Vanuatu",)*2,
        ("Vatican City",)*2,
        ("Venezuela",)*2,
        ("Vietnam",)*2,
        ("Yemen",)*2,
        ("Zambia",)*2,
        ("Zimbabwe",)*2,
    )

    country=CharField(
        max_length=80,
        blank=True,
        null=True,
        choices=COUNTRY_CHOICES
    )

    def __repr__(self): return self.address1
    def __str__(self): return repr(self)

class Invitation(Model):
    day=BooleanField(default=False)
    night=BooleanField(default=True)
    address=ForeignKey(Address, related_name="invitation")
    rsvp=BooleanField(default=False)
    password=CharField(max_length=13, blank=True, null=True)

    def __repr__(self):
        people=", ".join([repr(p) for p in self.person.all()])
        return people+": "+repr(self.address)

    def __str__(self): return repr(self)

    @staticmethod
    def makePassword():
        length=13
        chars=string.ascii_letters+string.digits+'!@#$%^&*()'
        random.seed=os.urandom(1024)
        return ''.join(random.choice(chars) for i in xrange(length))

    def save(self, *args, **kwargs):
        if self.password is None:
            self.password=Invitation.makePassword()
        super(Invitation, self).save(*args, **kwargs)

    def label(self):
        def groupPeople(people):
            sortkey=lambda person: " ".join((person.lastName, person.firstName))
            groupkey=lambda person: person.lastName
            sortedPeople=sorted(people, key=sortkey)
            return {k:tuple(g) for k,g in groupby(sortedPeople,groupkey)}
        
        agroups=[]
        for key,group in groupPeople(self.person.all()).items():
            names=[p.firstName for p in group]
            if len(names)==1: nameStr=names[0]
            else: nameStr=" & ".join([", ".join(names[:-1]), names[-1]])
            agroups.append("{0} {1}".format(nameStr, key))

        labelStr=" and ".join(agroups)

        for i in xrange(1,6):
            line=getattr(self.address, "address{0}".format(i))
            if len(line): labelStr="{0}\n{1}".format(labelStr,line)
            
        townCity=self.address.townCity
        if len(townCity): labelStr="{0}\n{1}".format(labelStr,townCity)

        labelStr="{0}\n{1}".format(labelStr,self.address.county)
        labelStr="{0}\n{1}".format(labelStr,self.address.postCode)
        return labelStr

    def getQRCode(self):
        url="http://www.andrinaandrob.co.uk/rsvp/{0}".format(self.pk)
        qr=QRCode(version=None, error_correction=ERROR_CORRECT_H, border=1)
        qr.add_data(url)
        qr.make(fit=True)
        return qr.make_image()

class MealOption(Model):
    description=CharField(max_length=512)

    COURSE_CHOICES=(
        ('starter',)*2,
        ('main',)*2,
        ('dessert',)*2,
    )

    course=CharField(max_length=20, choices=COURSE_CHOICES, blank=True, null=True)

    def __repr__(self):
        return "{0}: {1}".format(self.course, self.description)

    def __str__(self): return self.description

class Meal(Model):
    starter=ForeignKey('MealOption', related_name='starter', blank=True, null=True, on_delete=SET_NULL)
    main=ForeignKey('MealOption', related_name='main', blank=True, null=True, on_delete=SET_NULL)
    dessert=ForeignKey('MealOption', related_name='dessert', blank=True, null=True, on_delete=SET_NULL)

class Table(Model):
    name=CharField(max_length=32)
    shortName=CharField(max_length=3)
    topTable=BooleanField(default=False)

    def __repr__(self):
        return "{0} ({1})".format(self.name, self.shortName)

    def __str__(self): return repr(self)

class TablePosition(Model):
    class Meta:
        unique_together=('table','position')

    def __repr__(self):
        return "{0}: {1}".format(str(self.table), self.position)

    def __str__(self): return repr(self)

    table=ForeignKey('Table', related_name='position', blank=True, null=True, on_delete=SET_NULL)
    position=IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
