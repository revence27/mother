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
from mr.utils import mr_autoreg

class Command(BaseCommand):
  def handle(self, **options):
    con = Connection.objects.filter(identity = '256772344681')[1]
    spg = ScriptProgress.objects.all()[0]
    mr_autoreg(**{'connection': con, 'sender': spg})
