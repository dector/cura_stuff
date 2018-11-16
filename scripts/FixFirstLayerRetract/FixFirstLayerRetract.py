from typing import Optional, Tuple

from UM.Logger import Logger
from ..Script import Script

class FixFirstLayerRetract(Script):

    _line_count_tag = ';LAYER_COUNT:'

    def __init__(self):
        super().__init__()

    def getSettingDataString(self):
        return """{
            "name":"Fix First Layer Retract",
            "key": "FixFirstLayerRetract",
            "metadata": {},
            "version": 2,
            "settings": {}
        }"""

    def execute(self, data: list):
        first_layer_index = self._find_first_layer_index(data)

        if first_layer_index != -1:
            lines = data[first_layer_index].split('\n')

            i = self._find_line_index_startswith(self._line_count_tag, lines)

            if i != -1 and i-2 >= 0 and lines[i-2].strip() == 'G92 E0':
                lines[i-1] = self._with_disabled_rectraction(lines[i-1])
                data[first_layer_index] = '\n'.join(lines)

        return data

    def _find_first_layer_index(self, data: list):
        for i, layer in enumerate(data):
            if self._line_count_tag in layer:
                return i
        return -1

    def _find_line_index_startswith(self, what, where):
        for i, s in enumerate(where):
            if s.startswith(what):
                return i

    def _with_disabled_rectraction(self, s):
        parts = s.strip().split(' ')

        is_move_command = parts[0] == 'G1' or parts[0] == 'G0'
        if not is_move_command:
            return False

        return ' '.join([p for p in parts if not p.startswith('E-')])
