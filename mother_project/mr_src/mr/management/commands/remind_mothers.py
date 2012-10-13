#!  /usr/bin/env python
# encoding: UTF-8
# vim: ts=2
from datetime import datetime, timedelta
import itertools
from django.db.models import Q
from django.core.management.base import BaseCommand
import os
import sys
import Queue
from rapidsms.models import Contact, Connection, Backend
from rapidsms_httprouter.models import Message
from rapidsms.messages.outgoing import OutgoingMessage
from mr.models import ReminderMessage
from script.models import ScriptProgress, Script

class Command(BaseCommand):
  def handle(self, **options):
    outmsgs = ReminderMessage.as_hash()
    for week in outmsgs.keys():
      this_week = outmsgs[week]
      for day in this_week.keys():
        mother_queue  = Queue.Queue()
        this_day      = this_week[day]
        # for mother in Contact.objects.raw('''SELECT * FROM rapidsms_contact WHERE ((NOW() :: DATE) - ('%d WEEK %d DAY' :: INTERVAL)) :: DATE = last_menses :: DATE''' % (week, day)):
        # for mother in Contact.objects.raw('''SELECT * FROM rapidsms_contact WHERE (last_menses + ('%d WEEK %d DAY' :: INTERVAL)) :: DATE = NOW() :: DATE''' % (week, day)):
        # Because Django ORM speaks pidgin: “today” will be encoded as “between end of yesterday and start of tomorrow”. Hahaha. As long as it is not SQL.
        # back_then = datetime.now() - timedelta(weeks = week, days = day)
        # prior_day = back_then - timedelta(days = 1)
        # mothers   = Contact.objects.filter(interested = True, last_menses__range = (prior_day, back_then)).exclude(connection = None)
        mothers   = Contact.objects.raw('''SELECT * FROM rapidsms_contact WHERE ((NOW() :: DATE) - ('%d WEEK %d DAY' :: INTERVAL)) :: DATE = last_menses :: DATE''' % (week, day - 1))
        sending   = []
        for mother in mothers:
          if not mother.default_connection:
            continue
          sending.append(mother.default_connection.identity)
          msg     = Message.objects.create(connection = mother.default_connection, status = 'Q', direction = 'O', text = this_day)
          # msg.save() or sys.stderr.write('FAILED.\n')
          if msg:
            sys.stderr.write('%s (%s)\n' % (mother.default_connection.identity, mother.last_menses.strftime('%d-%m-%Y')))
          else:
            if sys.stderr.isatty():
              sys.stderr.write('FAILED.\n') # Colorise?
            else:
              sys.stderr.write('FAILED.\n')
        if sending:
          sys.stderr.write('Sending to %d mothers (week %d, day %d):\n%s\n\n%s\n' % (len(sending), week, day, this_day, ', '.join(sending)))
          sys.stderr.write('\n' + ('==' * 12) + '\n')
