---
title: expensive imports in GUIs
layout: post
---

I maintain an application called [Circleguard](https://github.com/circleguard/circleguard), written in python + pyqt. The challenges of distributing a python gui application are numerous and I wouldn't do it again given the choice. But an interesting problem did come up as a result, which is, as the title of this blog post suggests, how to import expensive modules without impacting the user's experience.

Circleguard relies on several hard hitting libraries behind the scenes, notably numpy, scipy, and matplotlib. All told, importing these modules takes about 0.8 seconds. Not awful, but nothing to sneeze at, especially because a naive import will freeze the ui. Here's a snippet from the code with matplotlib as an example, though similar scenarios occur with the other libraries mentioned:

```python
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT

class FrametimeWindow(QMainWindow):
    def __init__(self, replay):
        super().__init__()

        self.setWindowTitle("Replay Frametime")
        self.setWindowIcon(QIcon(resource_path("logo/logo.ico")))

        frametime_graph = FrametimeGraph(replay)
        self.addToolBar(NavigationToolbar2QT(frametime_graph.canvas, self))
        self.setCentralWidget(frametime_graph)
        self.resize(600, 500)
```

Since the import is at the top of the file, this import will whenever the application first starts, and block the ui thread until the import is complete. That's 0.8 seconds added to the time it takes for circleguard to launch every time!

How can we alleviate this? The most obvious answer is to simply move the import, assuming you're not calling any methods when the application first starts which import these expensive modules:

```python
class FrametimeWindow(QMainWindow):
    def __init__(self, frametime_graph):
        super().__init__()
        from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
        self.setWindowTitle("Replay Frametime")
        self.setWindowIcon(QIcon(resource_path("logo/logo.ico")))

        self.addToolBar(NavigationToolbar2QT(frametime_graph.canvas, self))
        self.setCentralWidget(frametime_graph)
        self.resize(600, 500)
```

This is an improvement, but all we've really done is defer the cost of importing until these methods are called for the first time, instead of when the application starts. Users will still experience a noticable freeze in the ui when taking certain actions which cause these methods to be hit.

The solution I came up with on top of this is to still import all of the modules when the program starts, but *in a separate thread*. This ensures it won't block the main thread and ui actions, while also making sure the modules have already been imported when our functions need them, so that no additional cost will be incurred later on.

Here's what that looks like:

```python
def import_expensive_modules():
    # probably not necessary to import every single class, but better safe than
    # sorry.
    # pylint: disable=unused-import
    from circleguard import (Circleguard, KeylessCircleguard, LoadableContainer,
        Map, User, MapUser, Replay, ReplayMap, ReplayPath, Mod, Loader,
        Snap, Hit, Span, replay_pairs)
    from circlevis import BeatmapInfo, Visualizer, VisualizerApp
    from slider import Library, Beatmap
    from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
    from matplotlib.backends.backend_qt5agg import FigureCanvas # pylint: disable=no-name-in-module
    from matplotlib.figure import Figure
    import numpy as np
    # requests isn't that expensive, but might as well load it here anyway
    import requests
    # pylint: enable=unused-import

thread = threading.Thread(target=import_expensive_modules)
thread.start()
```

And it works like a charm. Since python imports are thread safe, we don't need to worry about weirdness caused by simultaneous imports (eg in this thread and the ui thread) or anything like that.

I think this is a pretty simple trick all things considered. But I haven't seen it mentioned anywhere online, which is why I'm bothering to write about it. Sticking expensive computations into a background thread is pretty standard practice, but since I don't normally consider importing modules as something that can happen anywhere except the main thread, it wasn't obvious to me that this could apply to importing modules as well.
