"""Offline tests: no Raspberry Pi, camera or servos needed."""
import sys
import types
import unittest
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import navigation  # noqa: E402

H, W = 480, 640  # the report's thresholds assume a 640x480 frame


def edge_map(rows_by_third):
    """Builds a Canny-style edge image with a horizontal edge at a given row in each third (None = clear)."""
    edges = np.zeros((H, W), dtype=np.uint8)
    third = W // 3
    for k, row in enumerate(rows_by_third):
        if row is not None:
            edges[row, k * third:(k + 1) * third] = 255
    return edges


class DecisionTests(unittest.TestCase):
    def decide(self, rows):
        action, _ = navigation.decide(navigation.scan_columns(edge_map(rows)))
        return action

    def test_clear_path_goes_forward(self):
        self.assertEqual(self.decide([None, None, None]), "Forward")

    def test_distant_obstacle_ahead_goes_forward(self):
        self.assertEqual(self.decide([None, 120, None]), "Forward")

    def test_close_obstacle_turns_toward_open_left(self):
        self.assertEqual(self.decide([None, 400, 300]), "Left")

    def test_close_obstacle_turns_toward_open_right(self):
        self.assertEqual(self.decide([300, 400, None]), "Right")

    def test_scan_finds_nearest_edge_from_bottom(self):
        edges = np.zeros((H, W), dtype=np.uint8)
        edges[100, :] = 255
        edges[350, :] = 255
        points = navigation.scan_columns(edges)
        self.assertTrue(all(y == 350 for _, y in points))


class HardwareImportTests(unittest.TestCase):
    def test_locomotion_import_does_not_touch_the_servo_driver(self):
        calls = []
        fake = types.ModuleType("Adafruit_PCA9685")
        fake.PCA9685 = lambda *a, **k: calls.append("created")
        sys.modules["Adafruit_PCA9685"] = fake
        try:
            sys.modules.pop("locomotion", None)
            import locomotion  # noqa: F401
            self.assertEqual(calls, [])
        finally:
            sys.modules.pop("Adafruit_PCA9685", None)


if __name__ == "__main__":
    unittest.main()
