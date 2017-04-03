from django.core.management.base import BaseCommand, CommandError
from amr.models import AmrEntry

class Command(BaseCommand):
    help = 'Reads the AMRs out of the specified AMR file and puts them into the database'
    
    def add_arguments(self, parser):
        parser.add_argument('filename')

    def handle(self, *args, **options):
        print(options['filename'])
