from django.core.management.base import BaseCommand
from faker import Faker
import random
from users.models import User
from django.utils import timezone

class Command(BaseCommand):
    help = 'Populates the database with random operation data'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Get the list of existing User IDs to link operations
        user_ids = User.objects.values_list('ID', flat=True)

        # Populate the operation table with random data
        for _ in range(1000):  # Adjust the number as needed
            # Randomly select one of the operation types
            operation_type = random.choice(['a', 'w'])

            # Random money used in the operation
            money_used = round(random.uniform(0, 5000), 2)

            # Random processing stage
            processing_stage = random.choice(['1', '2', '3'])

            # Randomly pick a user ID
            user_id = random.choice(user_ids)

            # Randomly generate times
            time_started = fake.date_time_this_year()
            # Ensure the datetime is in the correct format
            time_started_str = time_started.strftime('%Y-%m-%d %H:%M:%S')

            # For time_completed, set None or generate another random time if processing_stage == '3' (Completed)
            if processing_stage == '3':
                time_completed = fake.date_time_this_year()
                time_completed_str = time_completed.strftime('%Y-%m-%d %H:%M:%S')
            else:
                time_completed_str = None



            # Create the operation record using SQL insert
            from django.db import connection
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO operation (Money_Used, Proccesing_Stage, Operation_Type, User_ID, Time_started, Time_Completed)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, [money_used, processing_stage, operation_type, user_id, time_started_str, time_completed_str])

        self.stdout.write(self.style.SUCCESS('Operations populated successfully!'))
