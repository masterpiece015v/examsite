from django.conf import settings
import os

path = os.path.join(settings.BASE_DIR,'django.log')

def log_write( text ):
    with open( path , mode='a') as f:
        f.write( "%s\n"%text )