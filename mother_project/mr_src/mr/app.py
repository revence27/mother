from rapidsms.apps.base import AppBase
from django.conf import settings
from script.models import Script, ScriptProgress, ScriptSession
from rapidsms.models import Contact, Connection
from rapidsms_httprouter.models import Message
from datetime import datetime, timedelta
import re

class App (AppBase):

    def handle (self, message):
        escargot = 'mrs_autoreg'
        match    = None
        matched  = None
        for keywd in settings.KEYWORDS_AND_SLUGS:
            match = re.match(keywd, message.text, re.IGNORECASE)
            if match:
                escargot     = settings.KEYWORDS_AND_SLUGS[keywd]
                matched      = message.text[len(match.group(0)):]
                #message.text = matched
                break
        if escargot == 'mrs_opt_out':
          if not message.connection.contact:
            # Stop sending you nothing? :-p
            return False
          sps = ScriptProgress.objects.filter(connection = message.connection)
          sps.delete()
          sps = ScriptSession.objects.filter(connection = message.connection)
          sps.delete()
          message.connection.contact.interested = False
          message.connection.contact.save()
          # ScriptProgress.objects.create(
          #      script = Script.objects.get(slug = escargot),
          #  connection = message.connection)
          msg = Message(connection = message.connection, status = 'Q', direction = 'O', text = 'You will no longer receive FREE messages from Mother Reminder. If you want to join again please send JOIN to 6400.')
          msg.save()
          return False
        if (not message.connection.contact) or (not ScriptProgress.objects.filter(connection = message.connection)):
            # if match:
            if True:  # Any word goes for registration.
                message.connection.contact = Contact.objects.create(name  = 'Anonymous User')
                message.connection.contact.interested  = True
                message.connection.contact.last_menses = datetime.now() - timedelta(days = 42)
                message.connection.contact.save()
                message.connection.save()
                ScriptProgress.objects.create(
                        script = Script.objects.get(slug = escargot),
                    connection = message.connection)
            else:
                msg =  Message(connection = message.connection, status = 'Q', direction = 'O', text = "You just contacted Mother Reminder. Did you know that pregnant women should go to the health facility 4 times during preganancy? Stay Healthy!")
                msg.save()
            return False
        else:
          if match and escargot == 'mrs_autoreg':
            msg = Message(connection = message.connection, status = 'Q', direction = 'O', text = "You are already registered with Mother Reminder and will receive free health info. Reply with STOP to leave Mother Reminder. Re-join by sending JOIN to 6400.")
            msg.save()
          else:
            if ScriptProgress.objects.filter(connection = message.connection, step__order = 5):
              msg = Message(connection = message.connection, status = 'Q', direction = 'O', text = "You just contacted Mother Reminder. Did you know that pregnant women should go to the health facility 4 times during preganancy? Stay Healthy!")
              msg.save()
        return False
