from os.path import getmtime
import datetime, io
from json import dumps, loads

import Image

from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.utils import ImageReader

from django.shortcuts import render_to_response, HttpResponse, redirect
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.db.models import Q
from django.forms.models import inlineformset_factory

from .models import *
from .forms import *

TSFILE="./updates.txt"

def drawMultiString(c, x, y, s):
    for ln in s.split('\n'):
        c.drawString(x, y, ln)
        y-=c._leading
    return y

def touchDate():
    return datetime.datetime.fromtimestamp(getmtime(TSFILE))

def datedResponse(template, request, **kwargs):
    kwargs["touchDate"]=touchDate()
    return render_to_response(
        template,
        kwargs,
        context_instance=RequestContext(request)
    )

def index(request):
    return render_to_response(
        'index.html',
        context_instance=RequestContext(request)
    )

def home(request):
    return datedResponse("home.html", request)

def venue(request):
    return datedResponse("venue.html", request)

def travel(request):
    return datedResponse("travel.html", request)

def accommodation(request):
    return datedResponse("accommodation.html", request)

def contact(request):
    form=None
    if request.method=="POST":
        subject=request.POST.get('subject','')
        message=request.POST.get('message','')
        fromEmail=request.POST.get('email', '')
        try: send_mail(subject, message, fromEmail, ['rob@gulon.co.uk'])
        except BadHeaderError: return HttpResponse("Invalid Header Found!")
    else: form=ContactForm()
    return datedResponse("contact.html", request, form=form)

@login_required
def createPerson(request):
    people=Person.objects.all()

    invitation_count=Invitation.objects.all().count()
    rsvp_count=Invitation.objects.filter(rsvp=True).count()

    day_count=Person.objects.filter(Q(invitation__day=True) & Q(weddingParty=False) & Q(child=False)).count()
    day_attending_count=Person.objects.filter(Q(attendingDay=True) & Q(weddingParty=False) & Q(child=False)).count()

    night_count=Person.objects.filter(invitation__night=True).count()
    night_attending_count=Person.objects.filter(attendingNight=True).count()

    weddingParty_count=Person.objects.filter(weddingParty=True).count()
    child_count=Person.objects.filter(child=True).count()

    if request.method=="POST":
        pForm=PersonForm(request.POST)
        if pForm.is_valid(): pForm.save()
    else: pForm=PersonForm()

    return render_to_response(
        'createPerson.html',
        {
            "pForm":pForm,
            'people':people,
            'day_count': day_count,
            'day_attending_count': day_attending_count,
            'night_count': night_count,
            'night_attending_count': night_attending_count,
            'weddingParty_count': weddingParty_count,
            'child_count': child_count,
            'invitation_count': invitation_count,
            'rsvp_count': rsvp_count,
        },
        context_instance=RequestContext(request)
    )

@login_required
def createAddress(request):
    addresses=Address.objects.all()

    if request.method=="POST":
        aForm=AddressForm(request.POST)
        if aForm.is_valid(): aForm.save()
    else: aForm=AddressForm()

    return render_to_response(
        'createAddress.html',
        {"aForm":aForm, 'addresses':addresses},
        context_instance=RequestContext(request)
    )

@login_required
def createInvitation(request):
    invitations=Invitation.objects.all()

    if request.method=="POST":
        iForm=InvitationForm(request.POST)
        if iForm.is_valid():
            invitation=iForm.save()
            for pk in request.POST.getlist('people'):
                person=Person.objects.get(pk=pk)
                person.invitation=invitation
                person.save()
    else: iForm=InvitationForm()

    return render_to_response(
        'createInvitation.html',
        {"iForm":iForm, "invitations":invitations},
        context_instance=RequestContext(request)
    )

@login_required
def getPeopleForAddress(request):
    if request.is_ajax():
        if request.method=="POST":
            pk=request.POST['pk']
            addr=Address.objects.get(pk=pk)
            people=Person.objects.filter(address=addr)
            data=[{"id":p.pk, "name":repr(p)} for p in people]
        return HttpResponse(dumps({"people":data}), mimetype="application/json")

@login_required
def createSaveTheDates(request):
    invitations=Invitation.objects.filter(day=False)

    cpp=2#4
    cardWidth,cardHeight=14.8*cm,10.5*cm
    cardCount=len(invitations)
    pageCount=cardCount//cpp+(1 if cardCount%cpp else 0)

    fileName="./SaveTheDates.pdf"
    frontImage=settings.STATIC_ROOT+"img/postcard_front_black.png"
    backImage=settings.STATIC_ROOT+"img/postcard_back.png"

    m=3*cm
    positions=[
        (m, m,            cardWidth, cardHeight),
        (m, m+cardHeight, cardWidth, cardHeight),
    ]

    canvas=Canvas(fileName, pagesize=A4)

    for p in xrange(pageCount):
        for i in xrange(cpp):
            x,y,w,h=positions[i]
            canvas.drawImage(frontImage, x, y, w, h)

        canvas.setStrokeColorRGB(0.,0.,0.)
        canvas.setLineWidth(.5)
        canvas.setDash(2,2)

        canvas.line(m, m, m-cm, m)
        canvas.line(m, m-cm, m, m)

        canvas.line(cardWidth+m, m, cardWidth+m+cm, m)
        canvas.line(cardWidth+m, m-cm, cardWidth+m, m)

        canvas.line(m, cardHeight+m, m-cm, cardHeight+m)
        canvas.line(cardWidth+m, cardHeight+m, cardWidth+m+cm, cardHeight+m)

        canvas.line(m, (2*cardHeight)+m, m-cm, (2*cardHeight)+m)
        canvas.line(cardWidth+m, (2*cardHeight)+m, cardWidth+m+cm, (2*cardHeight)+m)

        canvas.line(m, (2*cardHeight)+m, m, (2*cardHeight)+m+cm)
        canvas.line(cardWidth+m, (2*cardHeight)+m, cardWidth+m, (2*cardHeight)+m+cm)

        canvas.showPage()

    count=0
    for p in xrange(pageCount):
        for i in xrange(cpp):
            x,y,w,h=positions[i]
            canvas.drawImage(backImage, x, y, w, h)

            canvas.setFont("Helvetica", 10)
            drawMultiString(
                canvas,
                x+cardWidth/2+(.5*cm),
                y+cardHeight/2,
                invitations[count].label()
            )
            count+=1
            if count==cardCount: break

        canvas.showPage()
    canvas.save()

    return render_to_response(
        'saveTheDates.html',
        context_instance=RequestContext(request)
    )

@login_required
def createInvitations(request):
    invitations=Invitation.objects.filter(day=True)

    cpp=4
    cardWidth,cardHeight=10.5*cm,14.8*cm
    cardCount=len(invitations)
    pageCount=cardCount//cpp+(1 if cardCount%cpp else 0)
    qrCodeSize=2*cm

    #fileName="./invitations.pdf"
    fileName="invitations.pdf"
    frontImage=settings.STATIC_ROOT+"img/rsvp-front.png"
    backImage=settings.STATIC_ROOT+"img/rsvp-back.png"

    positions=[
        (0,         0,          cardWidth, cardHeight),
        (0,         cardHeight, cardWidth, cardHeight),
        (cardWidth, 0,          cardWidth, cardHeight),
        (cardWidth, cardHeight, cardWidth, cardHeight),
    ]

    buffer=io.BytesIO()
    #canvas=Canvas(fileName, pagesize=A4)
    canvas=Canvas(buffer, pagesize=A4)

    for p in xrange(pageCount):
        for i in xrange(cpp):
            x,y,w,h=positions[i]
            canvas.drawImage(frontImage, x, y, w, h)

        canvas.showPage()

    count=0
    for p in xrange(pageCount):
        for i in xrange(cpp):
            x,y,w,h=positions[i]
            canvas.drawImage(backImage, x, y, w, h)

            canvas.setFont("Helvetica", 10)
            drawMultiString(
                canvas,
                x+(.8*cm),
                y+cardHeight-(1.25*cm),
                "To respond electronically please use the QR Code or\nURL and details below."
            )

            ## URL
            canvas.setFont("Helvetica-Bold", 10)
            canvas.drawString(x+(.8*cm), y+cardHeight-(2.5*cm), "URL:")
            canvas.setFont("Helvetica", 10)
            canvas.drawString(x+(1.7*cm), y+cardHeight-(2.5*cm), "http://www.andrinaandrob.co.uk/rsvp")

            ## Invitation ID
            canvas.setFont("Helvetica-Bold", 10)
            canvas.drawString(x+(.8*cm), y+cardHeight-(3*cm), "Invitation ID:")
            canvas.setFont("Helvetica", 10)
            canvas.drawString(x+(3.*cm), y+cardHeight-(3*cm), str(invitations[count].pk))

            ## Password
            canvas.setFont("Helvetica-Bold", 10)
            canvas.drawString(x+(.8*cm), y+cardHeight-(3.5*cm), "Password:")
            canvas.setFont("Helvetica", 10)
            canvas.drawString(x+(2.7*cm), y+cardHeight-(3.5*cm), invitations[count].password)

            ## QR Code
            canvas.drawImage(
                ImageReader(invitations[count].getQRCode()._img),
                x+cardWidth-qrCodeSize-(.7*cm),
                y+cardHeight-qrCodeSize-(1.75*cm),
                qrCodeSize,
                qrCodeSize
            )

            drawMultiString(
                canvas,
                x+(.8*cm),
                y+cardHeight-(4.5*cm),
                "To respond by post please fill out the form below (with\nreference to the enclosed menu) and return in the\nenvelope provided."
            )

            canvas.setFont("Helvetica-Bold", 10)
            canvas.drawString(
                x+(.8*cm),
                y+cardHeight-(6*cm),
                "Guest"
            )

            canvas.drawString(
                x+(3.1*cm),
                y+cardHeight-(6*cm),
                "Attending"
            )

            canvas.drawString(
                x+(5.15*cm),
                y+cardHeight-(6*cm),
                "Starter"
            )

            canvas.drawString(
                x+(7.1*cm),
                y+cardHeight-(6*cm),
                "Main"
            )

            canvas.drawString(
                x+(8.6*cm),
                y+cardHeight-(6*cm),
                "Dessert"
            )

            canvas.setFont("Helvetica", 10)

            ## Attending
            canvas.saveState()
            canvas.translate(
                x+(3.55*cm),
                y+cardHeight-(8.*cm)
            )
            canvas.rotate(75)

            drawMultiString(
                canvas,
                0,
                0,
                "Day\n Night\n  Neither"
            )
            canvas.restoreState()

            ## Starter
            canvas.saveState()
            canvas.translate(
                x+(5.35*cm),
                y+cardHeight-(8.*cm)
            )
            canvas.rotate(75)

            drawMultiString(
                canvas,
                0,
                0,
                "Haggis\n Melon\n  None"
            )
            canvas.restoreState()

            ## Main
            canvas.saveState()
            canvas.translate(
                x+(6.87*cm),
                y+cardHeight-(8.*cm)
            )
            canvas.rotate(75)

            drawMultiString(
                canvas,
                0,
                0,
                "Chicken\n Lamb\n  Pasta\n   None"
            )
            canvas.restoreState()

            ## Dessert
            canvas.saveState()
            canvas.translate(
                x+(8.75*cm),
                y+cardHeight-(8.*cm)
            )
            canvas.rotate(75)

            drawMultiString(
                canvas,
                0,
                0,
                "Cheesecake\n Cranachan\n  None"
            )
            canvas.restoreState()

            ## People
            for i,p in enumerate(invitations[count].person.all()):
                canvas.drawString(
                    x+(.8*cm),
                    y+cardHeight-(9.*cm)-(i*.5*cm),
                    p.firstName
                )

                for o in (
                    3.5, 3.95, 4.4,
                    5.25, 5.7, 6.15,
                    6.8, 7.25, 7.7, 8.15,
                    8.7, 9.15, 9.6,

                        ):
                    canvas.circle(
                        x+(o*cm),
                        y+cardHeight-(8.85*cm)-(i*.5*cm),
                        .125*cm
                    )

            canvas.saveState()                    
            canvas.setStrokeColorRGB(0.6,0.6,0.6)
            canvas.setFillColorRGB(0.6,0.6,0.6)
            #canvas.setLineWidth(1.)
            canvas.setLineWidth(.75)

            for o in (4.9, 6.5, 8.45):
                vo=y+cardHeight-(5.75*cm)
                canvas.line(
                    x+(o*cm), vo, x+(o*cm), vo-((i+1)*.5*cm)-(2.85*cm)
                )

            canvas.restoreState()

            canvas.setFont("Helvetica", 10)
            drawMultiString(
                canvas,
                x+(.8*cm),
                y+(3.5*cm),
                "If you have any special requests, dietry requirements or\nwould like a childs meal provided for any of the above\nguests then please state below:"
            )            

            count+=1
            if count==cardCount: break

        canvas.showPage()            
    canvas.save()

    # return render_to_response(
    #     "base.html",
    #     context_instance=RequestContext(request)
    # )

    response=HttpResponse(content_type="application/pdf")
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(fileName)

    pdf=buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

@login_required
def createMeal(request):
    people=Person.objects.filter(attendingDay=True)

    mForm=MealForm()
    return render_to_response(
        'createMeal.html',
        {"mForm":mForm, 'people':people},
        context_instance=RequestContext(request)
    )


def createTables(request):
    tables=dict()
    for table in Table.objects.all():
        td=tables.setdefault(str(table), dict())
        for position in TablePosition.objects.filter(table=table).order_by('position'):
            name="{0} {1}".format(position.person.firstName, position.person.lastName)
            td[position.position]=name

    return render_to_response(
        'createTables.html',
        {'tables':tables},
        context_instance=RequestContext(request)
    )

def checkLogin(fn):
    def wrap(request, *args, **kwargs):
        if not request.session.get('invite_logged_in'):
            request.session['invite_pk']=kwargs.get('invitationNum',None)
            return login(request)
        return fn(request, *args, **kwargs)
    return wrap

@checkLogin
def rsvp(request, invitationNum=None):
    if invitationNum==None: invitationNum=request.session.get('invite_pk')
    invite=Invitation.objects.get(pk=invitationNum)

    fields=['firstName','lastName']
    if invite.day: fields+=['attendingDay']
    fields+=['attendingNight']

    RSVPFormset=inlineformset_factory(
        Invitation,
        Person,
        fields=fields,
        can_delete=False,
        max_num=invite.person.count()
    )

    if request.method=="POST":
        formset=RSVPFormset(request.POST, request.FILES, instance=invite)
        if formset.is_valid():
            formset.save()

            if invite.day:
                if invite.person.filter(attendingDay=True).count()>0:
                    return redirect('/meal/', context_instance=RequestContext(request))

            invite.rsvp=True
            invite.save()
            return redirect('/logout/',context_instance=RequestContext(request))
    else:
        formset=RSVPFormset(instance=invite)
    return render_to_response(
        'rsvp.html',
        {
            "invite":invite,
            'form':RSVPFormset(instance=invite)
        },
        context_instance=RequestContext(request)
    )

@checkLogin
def meal(request):
    invitationNum=request.session.get('invite_pk')
    invite=Invitation.objects.get(pk=invitationNum)

    forms=[]    
    if request.method=="POST":
        ok=True
        for p in invite.person.filter(attendingDay=True):
            prefix="person{0}".format(p.pk)
            form=MealForm(request.POST, instance=p.meal, prefix=prefix)
            if not form.is_valid(): ok=False
            else: form.save()

        if ok:
            invite.rsvp=True
            invite.save()
            return redirect('/logout/',context_instance=RequestContext(request))
    else:
        for p in invite.person.filter(attendingDay=True):
            prefix="person{0}".format(p.pk)
            if not p.meal:
                meal=Meal.objects.create()
                p.meal=meal
                p.save()
            forms.append(MealForm(instance=p.meal, prefix=prefix))
    return render_to_response('meal.html', {'forms':forms}, context_instance=RequestContext(request))

def login(request):
    if request.method=="POST":
        invite=Invitation.objects.get(pk=request.POST['inviteId'])
        if invite.rsvp:
            return redirect('/logout/',context_instance=RequestContext(request))
        if invite.password==request.POST['password']:
            request.session['invite_logged_in']=True
            request.session['invite_pk']=invite.pk
            return redirect(request.POST['next'], context_instance=RequestContext(request))

    return render_to_response(
            'login.html',
            {'next':request.path, 'invitationNum':request.session.get('invite_pk') or ''},
            context_instance=RequestContext(request)
        )

def logout(request):
    request.session['invite_logged_in']=False
    request.session['invite_pk']=None
    return render_to_response(
        'logout.html',
        context_instance=RequestContext(request)
    )