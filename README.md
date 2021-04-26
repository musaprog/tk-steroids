# Tk-steroids

Tk-steroids contains some useful GUI elements (tkinter/tk widgets)
such as a selection boxes or matplotlib integration
that keep reoccuring in my code elsewhere.

## Installing

```
pip install tk-steroids
```

## Usage

```python
from tk_steroids.MODULE import WIDGET
```

* elements
	* Listbox
	* TickboxFrame
	* DropdownList
	* Tabs
	* ButtonsFrame
* matplotlib
	* CanvasPlotter
	* SequenceImshow
* dialogs
	* TickSelect
* menumaker
	* MenuMaker

Most of the widgets inherit from `tk.Frame` and
use *grid* positioning system internally.
There are exceptions to this logic such as `MenuMaker` that creates
a menu from a class that is inheriting it (when calling *_connect*).

### Example 1

The following example adds `TickboxFrame` on the second `Tab` page 

```python
import tkinter as tk
from tk_steroids.elements import Tabs, TickboxFrame

root = tk.Tk()

my_tabs = Tabs(root, ['Page 1', 'Page 2', 'Page 3'])
my_tabs.grid()

boxes = TickboxFrame(my_tabs.tabs[1], ['a', 'b', "c"], ['Fancyname A', 'Fabolous B', 'Handsome C'])
boxes.grid()

root.mainloop()
```

### Example 2

This example shows how `CanvasPlotter` simplifies
[the matplotlib in Tk routine](https://matplotlib.org/stable/gallery/user_interfaces/embedding_in_tk_sgskip.html)


```python
import tkinter as tk
from tk_steroids.matplotlib import CanvasPlotter

root = tk.Tk()

plotter = CanvasPlotter(root)
plotter.grid()

# These are normal matplotlib figure and ax, also available
# - plotter.figure
# - plotter.ax
fig, ax = plotter.get_figax()

ax.plot([0,4,2])

# Calls FigureCanvasTkAgg draw-method
plotter.update()

root.mainloop()
```

For convinience, `CanvasPlotter` has also
its own *plot* and *imshow* methods.


## Other

In these 0.x.y versions, things can change quite a lot
(no guaranteed API stability).
