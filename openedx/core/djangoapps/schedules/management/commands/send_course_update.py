"""
Management command to send Schedule course updates
"""

import datetime
import pytz
from textwrap import dedent

from django.contrib.sites.models import Site

from openedx.core.djangoapps.schedules.management.commands import SendEmailBaseCommand
from openedx.core.djangoapps.schedules.tasks import ScheduleCourseNextSectionUpdate


class Command(SendEmailBaseCommand):
    """
    Command to send Schedule course updates
    """
    help = dedent(__doc__).strip()
    async_send_task = ScheduleCourseNextSectionUpdate
    log_prefix = 'Course Update'

    def handle(self, *args, ** options):
        print('handle args: {}'.format(args))
        current_date = datetime.datetime(
            *[int(x) for x in options['date'].split('-')],
            tzinfo=pytz.UTC
        )

        site = Site.objects.get(domain__iexact=options['site_domain_name'])
        override_recipient_email = options.get('override_recipient_email')

        # day_offset set to 1 as we'll always be looking for yesterday
        print("Calling async_send_task.enqueue from Command")
        self.async_send_task.enqueue(site, current_date, 1, override_recipient_email)
