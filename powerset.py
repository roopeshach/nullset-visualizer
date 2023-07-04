#
import tkinter as tk
import numpy as np
import random

def intersect(collection, items):
  """
  Adds items to collection if they are not already in collection.
  """
  for item in items:
    if sorted(item) not in collection:
      collection.append(sorted(item))
      

def powerset(myset):
  if not myset:
    return []
  # F (e, T) = { X ∪ {e} | X ∈ T }
  def F(e, myset):
    intermediary = []
    
    for outer in myset:
      new = [e]
      for inner in myset:
        if inner != e:
          new.append(inner)
      intermediary.append(new)
    return intermediary
# T = S\{e} (where \ means relative complement or subtraction)
    # P(S) = P(T) ∪ F ( e, P(T))
  T = []
  for item in myset:
      Tgroup = []
      for inneritem in myset:
        if inneritem != item:
          Tgroup.append(inneritem)
      T.append(Tgroup)
  sets = []
  for Tgroup in T:
      if Tgroup:
        intersect(sets, [Tgroup])
  for Tgroup in T:
    sublist = powerset(Tgroup)
    for item in myset:
      intersect(sets, F(item, myset))
    if sublist:
      intersect(sets, sublist)
  return sets

items = powerset(
  ['i', 't']
)
results = []
print(items)
for item in items:
  for subitem in item:
    results.append(subitem)
print(len(results))



def draw_circle(brackets):
    """
    Draws a circle using Tkinter for each set in the nested list of sets (brackets).
    """
    root = tk.Tk()
    root.title("Circle Drawing")
    
    # Get screen size
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Set canvas size to fit screen
    canvas_width = screen_width
    canvas_height = screen_height
    canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
    canvas.pack()

    def draw_nested_circle(brackets, x, y, radius):
      """
      Helper function to draw a circle and any nested circles inside it.
      """
      if isinstance(brackets, list):
          max_distance = radius
          num_circles = len(brackets)
          for i, inner_brackets in enumerate(brackets):
              angle = (2*i + 1) * (180 / num_circles) - 90
              dx = radius * 0.8
              dy = radius * 0.8
              inner_radius = draw_nested_circle(inner_brackets, x + dx * np.cos(np.radians(angle)), y + dy * np.sin(np.radians(angle)), radius/2)
              distance = np.sqrt(dx**2 + dy**2) + inner_radius
              if distance > max_distance:
                  max_distance = distance
          color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
          canvas.create_oval(x-max_distance, y-max_distance, x+max_distance, y+max_distance, outline=color)
          for i, inner_brackets in enumerate(brackets):
              angle = (2*i + 1) * (180 / num_circles) - 90
              dx = max_distance * 0.8
              dy = max_distance * 0.8
              draw_nested_circle(inner_brackets, x + dx * np.cos(np.radians(angle)), y + dy * np.sin(np.radians(angle)), radius/2)
      else:
          color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
          canvas.create_oval(x-radius, y-radius, x+radius, y+radius, outline=color)
      return radius


    # Draw main circle in center of screen
    main_radius = 200
    main_x = screen_width / 2
    main_y = screen_height / 2
    draw_nested_circle(brackets, main_x, main_y, main_radius)

    root.mainloop()


draw_circle(items)
