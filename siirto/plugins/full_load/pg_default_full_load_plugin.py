import os
import psycopg2

from siirto.plugins.full_load.full_load_base import FullLoadBase
from siirto.shared.enums import PlugInType


class PgDefaultFullLoadPlugin(FullLoadBase):
    """
    Postgres full load default plugin.
    """

    # plugin type and plugin name
    plugin_type = PlugInType.Full_Load
    plugin_name = "PGDefaultFullLoad"

    def __init(self,
               *args,
               **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def _set_status(self, status):
        self.status = status

    def execute(self):
        self._set_status("in progress - started")
        connection = psycopg2.connect(self.connection_string)
        cursor = connection.cursor()
        copy_query = f"\\COPY {self.table_name} TO program 'split -dl 1000000 " \
                     f"--a _{self.table_name}.csv' (format csv)"
        file_to_write = os.path.join(self.output_folder_location, f"{self.table_name}_full.csv")
        with open(file_to_write, "w") as output_file:
            cursor.copy_to(output_file, self.table_name)
        self._set_status("in progress - bulk file created")
        split_command = f'split -dl 1000000 {self.table_name}_full.csv --a _{self.table_name}.csv'
        os.system(split_command)
        self._set_status("in progress - smaller files created")
        self._set_status("completed")
        if self.notify_on_completion is not None:
            self.notify_on_completion(
                {
                    'status': 'success',
                    'table_name': self.table_name,
                    'error': None
                }
            )