
PICTURE_VIEW = """
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
"""
