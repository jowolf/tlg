import os

from django.core.management.base import BaseCommand, CommandError
from stheme.engine import YamlOperation, my_path, ops_path

trace = 1

if trace: print my_path, ops_path

class Command(BaseCommand):
    #args = '<poll_id poll_id ...>'
    help = 'Compiles and prepares the "Django-stheme" obdjects, meta-templates, and theme preparations, starting with "operations/themes.yaml".'
    can_import_settings = True

    def handle(self, *args, **options):
      os.chdir (os.path.join (my_path, ops_path))
      YamlOperation ('themes.yaml', None)()
      self.stdout.write ('Successfully compiled')
