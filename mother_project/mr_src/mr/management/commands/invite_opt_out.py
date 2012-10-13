#!  /usr/bin/env python
# vim: ts=2
# encoding: UTF-8

from optparse import OptionParser, make_option

from datetime import datetime, timedelta
import itertools
from django.db.models import Q
from django.core.management.base import BaseCommand
import os
import Queue
from rapidsms.models import Contact, Connection, Backend
from rapidsms_httprouter.models import Message
from rapidsms.messages.outgoing import OutgoingMessage
from mr.models import ReminderMessage
from script.models import ScriptProgress, Script

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
      make_option('-a', '--all',  dest = 'all'),
      make_option('-t', '--text', dest = 'text'),
    )

    def handle(self, **options):
        text    = options.get('text') or 'If you want to stop receiving FREE messages from Mother Reminder please reply with STOP.'
        outmsgs = ReminderMessage.as_hash().keys()
        outmsgs.sort()
        try:
            lastweek  = outmsgs[-1]
            query     = Contact.objects.filter(interested = True).exclude(connection  = None)
            if not options.get('all'):
              query.filter(last_menses__lt = (datetime.now() - timedelta(weeks=lastweek)))

            for mother in query:
                last_optout = Message.objects.filter(connection=mother.default_connection).filter(text=text).order_by('-date')
                message     = Message(connection  = mother.default_connection, direction  = 'O', status = 'Q', text = text)
                if not last_optout:
                    msg.save()
                else:
                    if last_optout[0].date + timedelta(weeks=8) <= datetime.now():
                        msg.save()

                        # msg.save()
                        # application, batch, connection, date, direction, flags, id, in_response_to, poll, poll_responses, priority, responses, status, submissions, text
        except IndexError:
            pass
