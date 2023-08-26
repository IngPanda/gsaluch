from datetime import datetime
def cron():
    print('Hola '+datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


cron()