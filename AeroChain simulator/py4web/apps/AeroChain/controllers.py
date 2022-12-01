"""
This file defines actions, i.e. functions the URLs are mapped into
The @action(path) decorator exposed the function at URL:

    http://127.0.0.1:8000/{app_name}/{path}

If app_name == '_default' then simply

    http://127.0.0.1:8000/{path}

If path == 'index' it can be omitted:

    http://127.0.0.1:8000/

The path follows the bottlepy syntax.

@action.uses('generic.html')  indicates that the action uses the generic.html template
@action.uses(session)         indicates that the action uses the session
@action.uses(db)              indicates that the action uses the db
@action.uses(T)               indicates that the action uses the i18n & pluralization
@action.uses(auth.user)       indicates that the action requires a logged in user
@action.uses(auth)            indicates that the action requires the auth object

session, db, T, auth, and tempates are examples of Fixtures.
Warning: Fixtures MUST be declared with @action.uses({fixtures}) else your app will result in undefined behavior
"""
import datetime

from py4web import action, Field, request, abort, redirect, URL
from yatl.helpers import A
from .common import db, session, T, cache, auth, logger, authenticated, unauthenticated, flash
from py4web.utils.form import *
from pydal.validators import IS_NOT_EMPTY
from py4web.utils.auth import Auth
from py4web import Flash
import re
import subprocess
@action("index")
@action.uses("index.html", auth)
def index():
    redirect(URL('index/0'))


@action("index/<flashMsg>")
@action.uses("index.html", auth, T, flash)
def index(visible=True, flashMsg=""):


    #error messages handled here
    if flashMsg is not "0":
        flashMsg = " ".join(flashMsg.split('_')) + "!"
        flash.set(flashMsg, _class="info", sanitize=True)

    #user authentication
    user = auth.get_user()
    counter = 0
    airline = "hidden"
    for row in db(db.setAirline.user_email == auth.current_user.get('email')).select():
        counter = counter + 1
        if row.approved == True:
            airline = True
    if counter is not 0:
        visible = "hidden"



    #return values
    message = T("Hello {first_name}".format(**user) if user else "Hello")
    actions = {"allowed_actions": auth.param.allowed_actions}
    return dict(message=message, actions=actions, visible=visible, airline=airline)



#registration form
@action('register', method=['GET', 'POST'])
@action.uses('minimal_form.html', auth)
def register():

    if (auth.get_user().get('email') is None):
        redirect(URL('index/Please_Log_In'))

    form = Form([Field('airline_name')])
    if form.accepted:
        counter = 0
        for row in db(db.setAirline.user_email == auth.current_user.get('email')).select():
            counter = counter + 1
        if counter is not 0:
            redirect(URL("index/You_already_filled_out_this_form"))
        else:
            db.setAirline.insert(user_email = auth.current_user.get('email'), airline_name= form.vars['airline_name'], datetime=datetime.datetime.utcnow())
            redirect(URL('accepted'))
    if form.errors:
        redirect(URL('not_accepted'))
    return dict(form=form)


@action('lookup', method=['GET', 'POST'])
@action.uses('lookup.html', auth)
def lookup():

    #check for authentication
    if (auth.get_user().get('email') is None):
        redirect(URL('index/Please_Log_In'))

    #initialize variables
    rows = []
    airline = "hidden"
    name = ""

    #form
    form = Form([Field('First_Name'), Field('Last_Name')])
    if form.accepted:

       #get most recent radix info
        for row in db(db.admin).select():
            account = row
        showNFTS = "resim show "+ account.component
        output = subprocess.getoutput(showNFTS)

        for line in output[output.find('Resources:'):].splitlines():
            nonFung = line[line.find('NonFungible'):]
            if nonFung[0] == "N":
                #nft data
                #example
                #("artour", "babaev", "not vaping", "2022-09-27T16:06")
                parameters = re.sub(r'[()]', '', nonFung[nonFung.find('immutable_data')+22:-26])
                print(parameters)
                parameters = parameters.split(",")
                for index, x in enumerate(parameters):
                    if x[0] == " ":
                        parameters[index] = x.replace(" ", "", 1)
                    parameters[index] = parameters[index].replace('"', "")

                if parameters[0] == form.vars['First_Name'] and parameters[1] == form.vars['Last_Name']:
                    rows.append({'First_Name': parameters[0], 'Last_Name': parameters[1], 'Reason': parameters[2]})

        #check if we are an airline
        counter = 0
        for row in db(db.setAirline.user_email == auth.current_user.get('email')).select():
            if row.approved is True:
                counter = counter + 1
        print(counter)
        if counter is not 0:
            airline = "visible"

        #if person not on do not fly list return persons name
        if len(rows) == 0:
            name = form.vars['First_Name'] + " " + form.vars['Last_Name']
        
    return dict(form=form, rows=rows, airline=airline, name=name)


#add user to do not fly list
@action('addToNoFly', method=['GET', 'POST'])
@action.uses('noFly.html', auth)
def register():
    if (auth.get_user().get('email') is None):
        redirect(URL('index/Please_Log_In'))

    MyStyle = FormStyleDefault
    MyStyle.classes = FormStyleDefault.classes
    MyStyle.widgets['Birth_Date']=DateTimeWidget()

    form = Form([Field('First_Name'), Field('Last_Name'), Field('Birth_Date'), Field('Reason')], formstyle=MyStyle)
    if form.accepted:

        
        #check if we are an airline
        counter = 0
        for row in db(db.setAirline.user_email == auth.current_user.get('email')).select():
            if row.approved is True:
                counter = counter + 1
        print(counter)
        if counter is not 0:
            db.doNotFly.insert(user_email_of_airline = auth.current_user.get('email'),
                First_Name= form.vars['First_Name'], 
                Last_Name= form.vars['Last_Name'], 
                Birth_Date= form.vars['Birth_Date'], 
                Reason= form.vars['Reason'], 
                datetime=datetime.datetime.utcnow())

            #add to DB (OLD)

            #create an NFT
            #3 lines to mint an nft

            #get radix info
            for row in db(db.admin).select():
                account = row
            print(account.account)
            print(account.package)
            print(account.component)
            print(account.admin_badge)
            line1 = "CALL_METHOD " + 'ComponentAddress("'+ account.account + '")' + ' "lock_fee" Decimal("10");'
            line2 = "CALL_METHOD " + 'ComponentAddress("'+ account.account + '")' + ' "create_proof" '+ 'ResourceAddress("'+ account.admin_badge +'");'
            line3 = "CALL_METHOD " + 'ComponentAddress("'+ account.component + '")' + ' "mint_nft" ' +'"'+form.vars['First_Name']+'"'+ '"'+form.vars['Last_Name']+'"'+'"'+form.vars['Reason']+'"'+'"'+form.vars['Birth_Date']+'";'
            f = open("createNFT.rtm", "w")
            f.write(line1)
            f.write("\n")
            f.write(line2)
            f.write("\n")
            f.write(line3)
            f.close()

            output = subprocess.getoutput("resim run createNFT.rtm")
            print(output)
            showNFTS = "resim show "+ account.component
            output = subprocess.getoutput(showNFTS)
            print(output)
            redirect(URL('accepted'))
        else:
            redirect(URL('not_accepted'))
    if form.errors:
        redirect(URL('not_accepted'))
    return dict(form=form)



@action("accepted")
def accepted():
    redirect(URL('index/form_accepted'))



@action("not_accepted")
def not_accepted():
    redirect(URL('index/form_not_accepted'))


@action("admin")
@action.uses("admin.html", auth)
def admin():   
    user = auth.get_user()
    print(auth.current_user.get('email'))
    if auth.current_user.get('email') != "admin@ucdavis.edu":
        redirect(URL("index/not_an_admin"))
    for row in db(db.setAirline).select():
        print(row)
    return dict(rows=db(db.setAirline).select())

@action("approve/<id>", method=['GET', 'POST'])
@action.uses("admin.html", auth)
def approve(id):
    user = auth.get_user()
    if auth.current_user.get('email') != "admin@ucdavis.edu":
        redirect(URL("index/not_an_admin"))
    else:
        for row in db(db.setAirline.id == id).select():
            if row.approved is True:
                row.update_record(approved = False)
            else:
                row.update_record(approved = True)   
        redirect(URL('admin'))



@action("superAdmin")
@action.uses(auth)
def superAdmin():   
    user = auth.get_user()
    print(auth.current_user.get('email'))
    if auth.current_user.get('email') != "admin@ucdavis.edu":
        redirect(URL("index/not_an_admin"))
    #for row in db(db.setAirline).select():
    #    print(row)

    print("Hello world")
    account = ""
    for row in db(db.admin).select():
        account = row.account
        #get most recent account info from DB
    showAccount = "resim show "+ account
    o1 = subprocess.getoutput(showAccount)
    print(o1)
    output = subprocess.getoutput("resim show component_sim1qtd98wym6xjcp0wff4fgd4jn8q5sc5k6sypn5mayqnrqq4jx72")
    print(output)
    return dict()


@action("formAdmin", method=['GET', 'POST'])
@action.uses("formAdmin.html", auth)
def formAdmin():   
    user = auth.get_user()
    print(auth.current_user.get('email'))
    if auth.current_user.get('email') != "admin@ucdavis.edu":
        redirect(URL("index/not_an_admin"))
    #for row in db(db.setAirline).select():
    #    print(row)

    form = Form([Field('account'), Field('package'), Field('component'), Field('admin_badge')])
    if form.accepted:
        db.admin.insert(account = form.vars['account'], package=form.vars['package'], component=form.vars['component'], admin_badge=form.vars['admin_badge'])
        redirect(URL('accepted'))
    if form.errors:
        redirect(URL('not_accepted'))
    return dict(form=form)