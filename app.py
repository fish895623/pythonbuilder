from array import array
import os
from hashlib import md5
from sqlite3 import connect


class Makefile:
    """
    This class is for incremental building by calculating checksum every
    building.

    Use sqlite3 for database.
    """

    def __init__(
        self,
        database: str = "test.db",
        table: str = "default_table",
    ):
        """
        Initialize data and create database table if not exist.

        Args:
            database (str, optional): Defaults to "test.db".
            table    (str, optional): Defaults to "default_table".
        """
        self.data = {}
        self.database = database
        self.table = table

        self.con = connect(database=self.database)
        self.cur = self.con.cursor()
        self.sqlite3_table_initial()

    def sqlite3_table_initial(self):
        """
        Create Database Table.
        """
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS %s (file TEXT, checksum TEXT)" % (self.table)
        )
        self.con.commit()

    def sqlite3_insert_data(self):
        """
        Insert or Update data in sqlite3 database.
        """
        for i in self.data:
            self.cur.execute(
                "INSERT OR REPLACE INTO '%s'(file, checksum) values('%s', '%s');"
                % (self.table, i, self.data[i]["checksum"])
            )
        self.con.commit()

    def dict_file_checksum(self, file: str):
        """
        Append to list with filename and checksum.

        Args:
            file (str): filename to get checksum.
        """
        self.data[file] = {
            "checksum": self.checksum(file=file),
        }

    def checksum(self, file: str) -> str:
        """
        Macro for make md5sum.

        Args:
            file (str): filename to get checksum.

        Returns:
            str: md5sum checksum.
        """
        return md5(open(file=file, mode="rb").read()).hexdigest()

    def file_list(self) -> array:
        """
        Make files only.

        Don't need directory to get checksum.

        Returns:
            array: files to get checksum.
        """
        files = []
        for r, d, f in os.walk("."):
            for file in f:
                files.append(os.path.join(r, file))

        return files


if __name__ == "__main__":
    a = Makefile()
    for i in a.file_list():
        a.dict_file_checksum(i)

    a.sqlite3_insert_data()

    a.cur.close()
    a.con.close()
