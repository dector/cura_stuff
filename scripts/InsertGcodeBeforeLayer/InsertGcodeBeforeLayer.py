from ..Script import Script

class InsertGcodeBeforeLayer(Script):
    def __init__(self):
        super().__init__()

    def getSettingDataString(self):
        return """{
            "name": "Insert GCode before layer",
            "key": "InsertGcodeBeforeLayer",
            "metadata": {},
            "version": 2,
            "settings":
            {
                "gcode":
                {
                    "label": "GCode",
                    "description": "GCode string to insert before layer. You can use `layer_number` for current layer number reference or `layers_count` for total layers number.",
                    "type": "str",
                    "default_value": ""
                }
            }
        }"""

    def execute(self, data: list):
        gcode = self.getSettingValueByKey("gcode")

        printed_layers = [(i, x) for i,x in enumerate(data) if ';LAYER:' in x]
        layers_count = len(printed_layers)
        
        current_layer = 0
        for index, layer in printed_layers:
            current_layer += 1
            
            lines = layer.split('\n')
            
            first_line_index = next((i for i,x in enumerate(lines) if ';LAYER:' in x), -1)
            if first_line_index != -1:
                line_to_insert = gcode.format(layer_number = current_layer, layers_count = layers_count)
                lines.insert(first_line_index + 1, line_to_insert)

                data[index] = '\n'.join(lines)

        return data
