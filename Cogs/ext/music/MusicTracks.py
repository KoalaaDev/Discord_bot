from pomice.objects import Track

class AutoTrack(Track):
    """A pomice track 
    that can differentiate between autoplay and searched tracks"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_autoplay = False