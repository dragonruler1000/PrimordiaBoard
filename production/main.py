import board

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.modules.layers import Layers
from kmk.modules.encoder import EncoderHandler
from kmk.extensions.peg_oled_Display import Oled, OledDisplayMode, OledReactionType

keyboard = KMKKeyboard()

# Pin configuration (based on your QMK config)
keyboard.col_pins = (board.GP28, board.GP29, board.GP0, board.GP3)
keyboard.row_pins = (board.GP4, board.GP2, board.GP1)
keyboard.diode_orientation = DiodeOrientation.COL2ROW

# Modules
layers = Layers()
encoder = EncoderHandler()
keyboard.modules = [layers, encoder]

# Encoder pins (from QMK config)
encoder.pins = ((board.GP26, board.GP27),)

# Define layers
layer_0 = [
    KC.VOLU, KC.MSTP, KC.MPLY, KC.MSEL,
    KC.VOLD, KC.MPRV, KC.MNXT, KC.EJCT,
    KC.MUTE, KC.MFFD, KC.MRWD, KC.NO,
]
layer_1 = [
    KC.F13, KC.F14, KC.F15, KC.F16,
    KC.F17, KC.F18, KC.F19, KC.F20,
    KC.F21, KC.F22, KC.F23, KC.F24,
]

keyboard.keymap = [layer_0, layer_1]

# Encoder behavior: Rotate to cycle layers
def rotate_layer_update(direction):
    current_layer = keyboard.active_layers[0]
    new_layer = (current_layer + 1) % len(keyboard.keymap) if direction else (current_layer - 1) % len(keyboard.keymap)
    keyboard.active_layers = [new_layer]

encoder.map = [
    ((lambda: rotate_layer_update(True), lambda: rotate_layer_update(False)),)
]

# OLED Extension
oled_ext = Oled(
    oled_addr=0x3C,              # Common I2C address for 0.91" OLEDs
    rotation=0,
    to_display=OledReactionType.LAYER,
    display_mode=OledDisplayMode.MASTER
)
keyboard.extensions.append(oled_ext)

# Customize what's displayed on the OLED
@oled_ext.on_render
def render_oled(oled):
    layer = keyboard.active_layers[0]
    layer_names = ["Media", "F-Keys"]
    oled.fill(0)
    oled.text("Layer:", 0, 0)
    oled.text(f"{layer} - {layer_names[layer]}", 0, 10)

if __name__ == '__main__':
    keyboard.go()
