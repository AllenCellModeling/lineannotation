from kivy.uix.scrollview import ScrollView


class XYScroll(ScrollView):
    def __init__(self, **kwargs):
        super(XYScroll, self).__init__(**kwargs)
        self.scroll_type = ['bars', 'content']


    # def update_from_scroll(self, *largs):
    #     print("largs: ", largs)
    #     print("scroll_x: ", self.scroll_x)
    #     print("scroll_y: ", self.scroll_y)

