import csv
from dataclasses import field
import datetime
from email import header
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from ...models import Diary

class Command(BaseCommand):
    help = "Backup Diary data"

    def handle(self, *args, **options):
        date=datetime.today().strftime("%Y%m%d")

        file_path = settings.BACKUP_PATH +'diary_' + date +'.csv'

        os.makedirs(settings.BACKUP_PATH ,exist_ok=True)

        with open(file_path,'w')as file:
            writer=csv.writer(file)

            header=[field.name for field in Diary._meta.fields]
            writer.writerow(header)

            diaries=Diary.objects.all()

            for diary in diaries:
                writer.writerow([str(diary.user),
                diary.title,
                diary.content,
                str(diary.photo1),
                str(diary.photo2),
                str(diary.photo3),
                str(diary.created_at),
                str(diary.updated_at)])

                files=os.listdir(settings.BUCKUP_PATH)

                if len(files)>=settings.NUM_SAVED_BUCKUP:
                    files.sort()
                    os.remove(settings.BACKUP_PATH+files[0])