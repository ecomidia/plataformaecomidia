from django.test import TestCase
import pandas as pd
from .models import Organization

# Create your tests here.

def populate():
    df = pd.read_csv('lista-organizações.csv')
    for row in df.itertuples():
        organization = Organization(
            organization = row[1],
            name = row[2],
            facebook_url = row[3],
            instagram_url = row[4],
            twitter_url = row[5],
        ).save()



