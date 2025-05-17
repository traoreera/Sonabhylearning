from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session
from datetime import datetime

class Task:
    """
    Gère les tâches planifiées
    """

    def __init__(self):
        """
        Initialise le scheduler
        """
        self.scheduler = BackgroundScheduler()

    def add_job(self, list_jobs=[dict]):
        """
        Ajoute une liste de tâches au scheduler

        :param list_jobs: liste de tâches à ajouter
        """
        try:
            for job in list_jobs: # type: ignore
                if job.get('activate', False): # type: ignore
                    self._add_job(job) # type: ignore
        except Exception as e:
            print(f"Erreur lors de l'ajout des tâches: {e}")

    def _add_job(self, job: dict): # type: ignore
        """
        Ajoute une tâche au scheduler

        :param job: tâche à ajouter
        """
        try:
            params:dict = {
                'func': job['fonction'],
                'trigger': job['interval'],
                'misfire_grace_time': job.get('misfire_grace_time', 30),
                'name': job['name'],
                'id': job['name']
            }

            if job['interval'] == 'interval':
                params['minutes'] = job.get('minutes', 10)
            elif job['interval'] == 'cron':
                params.update(job.get('cron_params', {}))  # Ajoute les paramètres de cron

            self.scheduler.add_job(**params)
        except Exception as e:
            print(f"Erreur lors de l'ajout de la tâche {job['name']}: {e}")

    def reload_jobs(self, list_jobs=[dict]):
        """
        Recharge les tâches avec les nouvelles paramètres

        :param list_jobs: liste de tâches à recharger
        """
        try:
            self.scheduler.shutdown(wait=False)
            self.scheduler = BackgroundScheduler()
            self.add_job(list_jobs)
            self.scheduler.start()
            print("Tâches rechargées avec succès")
        except Exception as e:
            print(f"Erreur lors du rechargement des tâches: {e}")