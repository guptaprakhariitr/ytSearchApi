
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from .views import ytplay
def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(ytplay,'interval', minutes=0.5)
    scheduler.start()