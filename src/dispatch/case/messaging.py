"""
.. module: dispatch.case.messaging
    :platform: Unix
    :copyright: (c) 2019 by Netflix Inc., see AUTHORS for more
    :license: Apache, see LICENSE for more details.
"""
import logging

from dispatch.database.core import SessionLocal
from dispatch.case.models import Case
from dispatch.messaging.strings import (
    CASE_CLOSE_REMINDER,
    CASE_TRIAGE_REMINDER,
    MessageType,
)
from dispatch.plugin import service as plugin_service


log = logging.getLogger(__name__)


def send_case_close_reminder(case: Case, db_session: SessionLocal):
    """
    Sends a direct message to the assignee reminding them to close the case if possible.
    """
    message_text = "Case Close Reminder"
    message_template = CASE_CLOSE_REMINDER

    plugin = plugin_service.get_active_instance(
        db_session=db_session, project_id=case.project.id, plugin_type="conversation"
    )
    if not plugin:
        log.warning("Case close reminder message not sent. No conversation plugin enabled.")
        return

    items = [
        {
            "name": case.name,
            "ticket_weblink": case.ticket.weblink,
            "title": case.title,
            "status": case.status,
        }
    ]

    plugin.instance.send_direct(
        case.assignee.individual.email,
        message_text,
        message_template,
        MessageType.case_status_reminder,
        items=items,
    )

    log.debug(f"Case close reminder sent to {case.assignee.individual.email}.")


def send_case_triage_reminder(case: Case, db_session: SessionLocal):
    """
    Sends a direct message to the assignee reminding them to triage the case if possible.
    """
    message_text = "Case Triage Reminder"
    message_template = CASE_TRIAGE_REMINDER

    plugin = plugin_service.get_active_instance(
        db_session=db_session, project_id=case.project.id, plugin_type="conversation"
    )
    if not plugin:
        log.warning("Case triage reminder message not sent. No conversation plugin enabled.")
        return

    items = [
        {
            "name": case.name,
            "ticket_weblink": case.ticket.weblink,
            "title": case.title,
            "status": case.status,
        }
    ]

    plugin.instance.send_direct(
        case.assignee.individual.email,
        message_text,
        message_template,
        MessageType.case_status_reminder,
        items=items,
    )

    log.debug(f"Case triage reminder sent to {case.assignee.individual.email}.")
