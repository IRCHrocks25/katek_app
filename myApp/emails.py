"""Outbound email helpers backed by Resend."""
import logging

from django.conf import settings
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)


def _site_url():
    return (settings.SITE_URL or 'http://localhost:8000').rstrip('/')


def send_welcome_email(user):
    """Send the welcome email to a newly-signed-up user.

    Returns True on success, False if Resend is not configured or the send fails.
    Failures are logged, never raised — signup must not block on email delivery.
    """
    if not getattr(settings, 'RESEND_API_KEY', ''):
        logger.info('RESEND_API_KEY not configured; skipping welcome email to %s', user.email)
        return False

    try:
        import resend
    except ImportError:
        logger.warning('resend package not installed; skipping welcome email')
        return False

    site_url = _site_url()
    first_name = (user.first_name or user.email.split('@', 1)[0] or 'there').strip()

    ctx = {
        'first_name': first_name,
        'email': user.email,
        'site_url': site_url,
        'login_url': site_url + '/login',
        'launchpad_url': site_url + '/launchpad',
        'privacy_url': site_url + '/privacy',
        'terms_url': site_url + '/terms',
        'support_email': 'support@katek.app',
        'logo_url': 'https://res.cloudinary.com/dcuswyfur/image/upload/v1776795634/katek_logo_white_p1evh7.svg',
    }

    html_body = render_to_string('emails/welcome.html', ctx)
    text_body = render_to_string('emails/welcome.txt', ctx)

    resend.api_key = settings.RESEND_API_KEY
    payload = {
        'from': settings.EMAIL_FROM,
        'to': [user.email],
        'reply_to': settings.EMAIL_REPLY_TO,
        'subject': 'Welcome to Katek — your workspace is ready',
        'html': html_body,
        'text': text_body,
    }

    try:
        resend.Emails.send(payload)  # type: ignore[arg-type]
        logger.info('Welcome email queued for %s', user.email)
        return True
    except Exception as exc:
        logger.warning('Failed to send welcome email to %s: %s', user.email, exc)
        return False
