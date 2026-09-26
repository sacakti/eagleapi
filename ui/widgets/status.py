from textual.widgets import Static

class StatusBar(Static):
   def on_mount(self):
       self.update(
           " Ready     ↑↓ Navigate     Enter Run     F2 Edit     Esc Exit "
       )