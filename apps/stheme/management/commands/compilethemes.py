import os

from django.core.management.base import BaseCommand, CommandError
from stheme.engine import YamlOperation, my_path

print my_path

class Command(BaseCommand):
    #args = '<poll_id poll_id ...>'
    help = 'Compiles and prepares the "Django-stheme" obdjects, meta-templates, and theme preparations, starting with "themes.yaml".'
    can_import_settings = True

    def handle(self, *args, **options):
      os.chdir (my_path)
      YamlOperation ('themes.yaml', None)()
      self.stdout.write ('Successfully compiled')