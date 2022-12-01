"""
This file defines the database models
"""
import datetime

from .common import db, Field, auth
from pydal.validators import *

### Define your table below
#
# db.define_table('thing', Field('name'))
#
## always commit your models to avoid problems later
#
# db.commit()
#
def get_user_email():
    return auth.current_user.get('email') if auth.current_user else None

def get_time():
    return datetime.datetime.utcnow()

db.define_table('setAirline',
                Field('user_email', default=get_user_email),
                Field('airline_name', 'text'),
                Field('ts', 'datetime', default=get_time),
                Field('approved', 'boolean', default=False)
                )


#    form = Form([Field('First_Name'), Field('Last_Name'), Field('Birth_Date'), Field('Reason')])

db.define_table('doNotFly',
                Field('user_email_of_airline', default=get_user_email),
                Field('First_Name', 'text'),
                Field('Last_Name', 'text'),
                Field('Birth_Date', 'text'),
                Field('Reason', 'text'),
                Field('ts', 'datetime', default=get_time),
                )


db.define_table('admin',
                Field('account', 'text'),
                Field('package', 'text'),
                Field('component', 'text'),
                Field('admin_badge', 'text')
                )

db.commit()