import djp
from django.core.management import (
    BaseCommand
)

class Command(BaseCommand):
    help = """
    Show the value of the DJP_PLUGIN_DIRS setting. This is where DJP looks
    for plugins formatted as *.py files.
    """
    def handle(self):
        if djp.plugins_dir:
            self.stdout.write(
                djp.plugins_dir,
                self.style.SUCCESS
           )
        else:
            self.stdout.write("No plugins dir.")

