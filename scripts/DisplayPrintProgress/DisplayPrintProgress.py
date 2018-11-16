from typing import Optional, Tuple

from UM.Logger import Logger
from ..Script import Script

class DisplayPrintProgress(Script):
    """This is simple post-processing script for Cura 3.5
    that displays information about printing progress on screen.

    Message that will be displayed in the beginning of each layer
    will display current layer, total number of layers and rough
    estimate about print progress.

    Example: "L 11/199 (6.7%)"
    """

    def __init__(self):
        super().__init__()

    def getSettingDataString(self):
        return """{
            "name":"Display Print Progress",
            "key": "DisplayPrintProgress",
            "metadata": {},
            "version": 2,
            "settings": {}
        }"""

    def execute(self, data: list):
        printed_layers = [[layer, layer.startswith(';LAYER:')] for layer in data]
        layers_count = len([x for x in printed_layers if x[1]])
        instructions_per_layer = [self._count_instructions(x) for x in printed_layers]
        total_instuctions = sum(instructions_per_layer)

        print_layer = 0
        used_instructions = 0
        for index, info in enumerate(printed_layers):
            if not info[1]:
                continue

            progress = used_instructions / total_instuctions
            print_layer += 1
            command = "M117 L {0}/{1} ({2:.1%})".format(print_layer, layers_count, progress)

            data[index] = command + '\n' + data[index]

            used_instructions += instructions_per_layer[index]

        return data

    def _is_command_line(self, s):
        stripped = s.lstrip()
        return stripped.startswith('G') or stripped.startswith('M') or stripped.startswith('T')

    def _count_instructions(self, info):
        if info[1]:
            s = info[0]
            return len([x for x in s.split('\n') if self._is_command_line(x)])
        else:
            return 0
