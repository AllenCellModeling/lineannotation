from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.image import Image
from .SarcomereLines import SarcomereLines

# View
Builder.load_string("""
<Picture>:
    # each time a picture is created, the image can delay the loading
    # as soon as the image is loaded, ensure that the center is changed
    # to the center of the screen.
    size: image.size
    size_hint: None, None
    Image:
        id: image
        source: root.source
        keep_ratio: True
        # create initial image to be 400 pixels width
        size: 2048, 2048

        # add shadow background
        canvas.before:
            Color:
                rgba: 1,1,1,1
            BorderImage:
                source: 'resources/shadow32.png'
                border: (36,36,36,36)
                size:(self.width+72, self.height+72)
                pos: (-36,-36)
""")


# Model
class Picture(Image):
    """
    Picture is the class that will show the image with a white border and a
    shadow. They are nothing here because almost everything is inside the
    picture.kv. Check the rule named <Picture> inside the file, and you'll see
    how the Picture() is really constructed and used.

    The source property will be the filename to show.

    The canvas is the object that takes drawing instructions, it's inherited from Image.
    """
    do_rotation = False
    do_scale = True
    source = StringProperty(None)

    def __init__(self, **kwargs):
        super(Picture, self).__init__(**kwargs)
        self.txt_name = kwargs["source"] + ".annot_txt"
        self.keep_points = SarcomereLines(self.txt_name)
        self.draw()
        self._modify = False  # this toggles the edit state
        self.magic_point = None

    def draw(self):
        self.keep_points.draw(self.canvas)

    def on_touch_down(self, touch):
        """
        This is a kivy hook. By defining this function on the Picture the picture
        responds to mouse clicks
        :param touch: this is the mouse down point, touch.pos are the image coordinates.
        """
        print("p:in on_touch_down")
        if self._modify:
            self.magic_point = touch.pos
            self.keep_points.highlight_nearest(self.magic_point, self.canvas)
        else:
            self.keep_points.add_point(touch)
            self.keep_points.write_file(self.txt_name, self.size)
            self.draw()

    def clear_line(self):
        print("p:clear_line")
        self.keep_points.undo_last()
        self.draw()

    def end_line(self):
        print("p:end_line")
        self.keep_points.end_line()

    def toggle_modify(self):
        print("p:toggle_modify")
        self._modify = not self._modify

    def set_remove(self):
        print("p:set_remove")
        if self._modify:
            self.keep_points.remove_nearest(self.magic_point, self.canvas)
            self.keep_points.draw(self.canvas)
            self.toggle_modify()
        self.draw()
