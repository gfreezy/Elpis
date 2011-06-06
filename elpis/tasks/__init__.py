import sys
sys.path.append('.')

from celery.task import task

@task
def send_mail(message):
    import mailer
    sender = mailer.Mailer('smtp.163.com')
    sender.login('gfreezy', 'qwertyuiop')
    sender.send(message)

