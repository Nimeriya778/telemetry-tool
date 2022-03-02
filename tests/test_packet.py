import unittest
from telemetry_tool.brd import BrdTelemetry
from telemetry_tool.chg import ChgTelemetry
from telemetry_tool.ldd import LddTelemetry
from telemetry_tool.pls import PlsTelemetry


class PacketTestCase(unittest.TestCase):
    def test_brd_load_from_packet(self) -> None:
        with open("test_file", "rb") as file:
            packet = file.read()
            brd = BrdTelemetry.load_from_packet(packet)
            self.assertAlmostEqual(brd.lt1, 11.992)

    def test_chg_load_from_packet(self) -> None:
        with open("test_file", "rb") as file:
            packet = file.read()
            chg = ChgTelemetry.load_from_packet(packet)
            self.assertAlmostEqual(chg.vtcur1, 0.2562)

    def test_ldd_load_from_packet(self) -> None:
        with open("test_file", "rb") as file:
            packet = file.read()
            ldd = LddTelemetry.load_from_packet(packet)
            self.assertAlmostEqual(ldd.ldout1, 106.272)

    def test_pls_load_from_packet(self) -> None:
        with open("test_file", "rb") as file:
            packet = file.read()
            pls = PlsTelemetry.load_from_packet(packet)
            self.assertAlmostEqual(pls.i1, 40.6589, places=4)


if __name__ == "__main__":
    unittest.main()
