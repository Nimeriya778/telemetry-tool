import unittest
from telemetry_tool.db import drop_table, create_table, insert_into_table
from telemetry_tool.queries_data import retrieve_from_db
from telemetry_tool.packet import get_telemetry
import sqlite3


class DatabaseTestCase(unittest.TestCase):
    def test_create_table(self) -> None:
        with open("test_file", "rb") as file:
            conn = sqlite3.connect(":memory:")
            create_table(conn, get_telemetry(file))
            result = conn.execute(
                "SELECT count(name) FROM sqlite_master WHERE type='table' AND name='LTU1_1'"
            )

            # If the count is 1, then table exists
            self.assertEqual(result.fetchone()[0], 1)

    def test_drop_table(self) -> None:
        with open("test_file", "rb") as file:
            conn = sqlite3.connect(":memory:")
            read_file = get_telemetry(file)
            create_table(conn, read_file)
            drop_table(conn, read_file)
            result = conn.execute(
                "SELECT count(name) FROM sqlite_master WHERE type='table' AND name='LTU1_1'"
            )

            # If the count is 0, then table doesn't exist
            self.assertEqual(result.fetchone()[0], 0)

    def test_insert_into_table(self) -> None:
        with open("test_file", "rb") as file:
            conn = sqlite3.connect(":memory:")
            read_file = get_telemetry(file)
            create_table(conn, read_file)
            insert_into_table(conn, read_file)
            result = conn.execute("SELECT cutime FROM LTU1_1")
            self.assertEqual(result.fetchone()[0], 1607312269)

    def test_retrieve_from_db(self) -> None:
        with open("test_file", "rb") as file:
            conn = sqlite3.connect(":memory:")
            read_file = get_telemetry(file)
            create_table(conn, read_file)
            insert_into_table(conn, read_file)
            result = retrieve_from_db(
                conn, ["cutime", "ldd_hv1", "ldd_ldout1"], "LTU1_1"
            )
            self.assertEqual(result.fetchone(), (1607312269, 209.844, 106.272))


if __name__ == "__main__":
    unittest.main()
