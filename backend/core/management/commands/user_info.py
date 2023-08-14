from django.core.management.base import BaseCommand
from twitter.models import Status
from datetime import datetime
import csv

class Command(BaseCommand):

	def handle(self, *args, **options):
		user_list = options['user_list']
		info = {'rt':[],'quote':[]}
		first_date = datetime(2022,8,1)
		last_date = datetime(2022,10,3)
		for user in user_list.split(','):
			senator_frist_date = Status.objects.filter(user__screen_name=user).latest('-created_at').created_at
			rts = Status.objects.filter(user__screen_name=user).filter(retweet_status__isnull=False).filter(created_at__gte=first_date).filter(created_at__lt=last_date).values('created_at','content','user__screen_name','retweet_status__user__screen_name')
			quotes = Status.objects.filter(user__screen_name=user).filter(quoted_status__isnull=False).filter(created_at__gte=first_date).filter(created_at__lt=last_date).values('created_at','content','user__screen_name','quoted_status__user__screen_name')	
			for rt in rts:
				info['rt'].append([rt['created_at'],rt['content'],rt['user__screen_name'],rt['retweet_status__user__screen_name']])
			for rt in quotes:
				info['quote'].append([rt['created_at'],rt['content'],rt['user__screen_name'],rt['quoted_status__user__screen_name']])
				
		with open('rt.csv', 'w') as f:
			# create the csv writer
			writer = csv.writer(f)
			header = ['created_at','content','source','target']
			writer.writerow(header)
			writer.writerows(info['rt'])

		with open('quote.csv', 'w') as f:
			# create the csv writer
			writer = csv.writer(f)
			header = ['created_at','content','source','target']
			writer.writerow(header)
			writer.writerows(info['quote'])
					
	def add_arguments(self, parser):
		parser.add_argument('user_list', type=str, help='User list')