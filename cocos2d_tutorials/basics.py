# Tutos taken from cocos2d website : http://python.cocos2d.org/doc/programming_guide/quickstart.html

import argparse
import cocos
import pyglet

DEFAULT_TUTO = 'eventstuto' # 'helloworld', 'actionstuto', 'eventstuto'

class HelloWorld(cocos.layer.Layer):
    """
    A simple app that shows a window saying Hello World
    """

    def __init__(self):
        # Always call super in the constructor
        super().__init__()

        # Creates a label to display text
        label = cocos.text.Label(
            'Hello, world',
            font_name='Calibri',
            font_size=32,
            anchor_x='center', anchor_y='center',
            position=((320, 240))
        )

        # Adds the label (which is a subclass of CocosNode) as a child of our layer node
        self.add(label)


class ActionTuto(cocos.layer.ColorLayer):
    """
    Now introduces the action. Actions can be applied to any coco nodes (layers, windows, sprites)
    """

    def __init__(self):
        # blueish color
        super().__init__(64, 64, 224, 255)

        # Creates a label to display text
        label = cocos.text.Label(
            'Hello, world',
            font_name='Calibri',
            font_size=32,
            anchor_x='center', anchor_y='center',
            position=((320, 240))
        )

        # Adds the label (which is a subclass of CocosNode) as a child of our layer node
        self.add(label)

        # Creates a sprite
        sprite = cocos.sprite.Sprite('bulbasaur.png')
        sprite.position = 320, 240
        sprite.scale = 3

        # Adds the sprite to our layer (z is its position in an axis coming out of the screen)
        self.add(sprite, z=1)

        # Creates a ScaleBy action
        scale = cocos.actions.ScaleBy(3, duration=2)

        # Apply the actions to our label and sprite
        label.do(cocos.actions.Repeat(scale + cocos.actions.Reverse(scale)))
        sprite.do(cocos.actions.Repeat(cocos.actions.Reverse(scale) + scale))


class KeyDisplay(cocos.layer.Layer):
    # If you want that your layer receives director.window events, you must set this variable to 'True'
    is_event_handler = True

    def __init__(self):
        super().__init__()

        self.text = cocos.text.Label("", x=100, y=280)

        # To keep track of which keys are pressed:
        self.keys_pressed = set()
        self.update_text()
        self.add(self.text)


    def update_text(self):
        key_names = [pyglet.window.key.symbol_string(k) for k in self.keys_pressed]
        text = 'Keys: ' + ','.join(key_names)

        # Update self.text
        self.text.element.text = text

    # EVENT HANDLERS
    def on_key_press(self, key, modifiers):
        """This function is called when a key is pressed.
        'key' is a constant indicating which key was pressed.
        'modifiers' is a bitwise-or of several constants indicating which
            modifiers are active at the time of the press (ctrl, shift, capslock, etc.)
        """
        self.keys_pressed.add(key)
        self.update_text()

    def on_key_release (self, key, modifiers):
        """This function is called when a key is released.

        'key' is a constant indicating which key was pressed.
        'modifiers' is a bitwise or of several constants indicating which
            modifiers are active at the time of the press (ctrl, shift, capslock, etc.)

        Constants are the ones from pyglet.window.key
        """

        self.keys_pressed.remove (key)
        self.update_text()


class MouseDisplay(cocos.layer.Layer):
    is_event_handler = True     #: enable director.window events

    def __init__(self):
        super( MouseDisplay, self ).__init__()

        self.posx = 100
        self.posy = 240
        self.text = cocos.text.Label('No mouse events yet', font_size=18, x=self.posx, y=self.posy )
        self.add(self.text)

    def update_text(self, x, y):
        text = 'Mouse @ %d,%d' % (x, y)
        self.text.element.text = text
        self.text.element.x = self.posx
        self.text.element.y = self.posy

    # EVENT HANDLERS
    def on_mouse_motion(self, x, y, dx, dy):
        """Called when the mouse moves over the app window with no button pressed
        (x, y) are the physical coordinates of the mouse
        (dx, dy) is the distance vector covered by the mouse pointer since the last call.
        """
        print(x,y)
        self.update_text(x, y)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        """Called when the mouse moves over the app window with some button(s) pressed
        (x, y) are the physical coordinates of the mouse
        (dx, dy) is the distance vector covered by the mouse pointer since the last call.
        'buttons' is a bitwise-or of pyglet.window.mouse constants LEFT, MIDDLE, RIGHT
        'modifiers' is a bitwise-or of pyglet.window.key modifier constants (values like 'SHIFT', 'OPTION', 'ALT')
        """
        self.update_text(x, y)

    def on_mouse_press(self, x, y, buttons, modifiers):
        """This function is called when any mouse button is pressed
        (x, y) are the physical coordinates of the mouse
        'buttons' is a bitwise-or of pyglet.window.mouse constants LEFT, MIDDLE, RIGHT
        'modifiers' is a bitwise-or of pyglet.window.key modifier constants(values like 'SHIFT', 'OPTION', 'ALT')
        """
        self.posx, self.posy = cocos.director.director.get_virtual_coordinates(x, y)
        self.update_text(x, y)


def args_check(args):
    """
    Just takes our args as input, manually check some conditions
    :param args: args
    :return: args
    """
    pass

    return args


if __name__ == '__main__':
    # Parse args
    parser = argparse.ArgumentParser()
    parser.add_argument('--tuto', default=DEFAULT_TUTO, choices=['helloworld', 'actionstuto', 'eventstuto'])
    args = args_check(parser.parse_args())

    # Initializes the director (whatever this does)
    cocos.director.director.init(width=1280, height=720, caption='Cocos Tutorial', resizable=True)

    # Instantiates our layer and creates a scene that contains our layer as a child
    if args.tuto == 'helloworld':
        main_scene = cocos.scene.Scene(HelloWorld())

    elif args.tuto == 'actionstuto':
        layer = ActionTuto()
        layer.do(cocos.actions.RotateBy(360, duration=10))
        main_scene = cocos.scene.Scene(layer)

    elif args.tuto == 'eventstuto':
        main_scene = cocos.scene.Scene(KeyDisplay(), MouseDisplay())

    # We run our scene
    cocos.director.director.run(main_scene)


