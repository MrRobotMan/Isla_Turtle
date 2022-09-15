from __future__ import annotations
import random
import tkinter as tk
import turtle
from typing import NamedTuple

points = NamedTuple(
    "points", [("left", int), ("right", int), ("top", int), ("bottom", int)]
)
STEP = 50


def quit() -> None:
    """Exit the program"""
    turtle.bye()


def color(turt: turtle.Turtle) -> None:
    """Set the turtle to a random color"""
    red = random.random()
    green = random.random()
    blue = random.random()
    turt.color(red, green, blue)


def get_heading(turt: turtle.Turtle) -> tuple[int, int]:
    """Returns the heading as an X, Y pair of ints (1 or 0)"""
    heading = turt.heading()
    heading_quadrant = heading // 90  # 0, 1, 2, 3
    heading_complex = 1j**heading_quadrant  # j**0 == 1+0j, j**1 == 0+1j
    x = int(heading_complex.real)
    y = int(heading_complex.imag)
    return (x, y)


def forward(turt: turtle.Turtle, grid: points) -> None:
    """Move forward if possible"""
    current_x, current_y = turt.position()
    heading_x, heading_y = get_heading(turt)
    new_x = round(current_x) + heading_x * STEP
    new_y = round(current_y) + heading_y * STEP
    if not grid.left <= new_x <= grid.right or not grid.bottom <= new_y <= grid.top:
        return
    # re-adjust to be on grid.
    turt.goto(new_x, new_y)


def turn_right(turt: turtle.Turtle) -> None:
    """Turn right 90 degrees"""
    turt.right(90)


def turn_left(turt: turtle.Turtle) -> None:
    """Turn left 90 degrees"""
    turt.left(90)


def change_speed(turt: turtle.Turtle, delta: int, speed_var: tk.IntVar) -> None:
    """Change the turtle speed in range 1, 10 inclusive"""
    current = turt.speed()
    new = current + delta
    if not 1 <= new <= 10:
        return
    turt.speed(new)
    speed_var.set(turt.speed())


def draw_grid(grid: points, width: int, height: int) -> None:
    """Draw the initial grid."""
    turt = turtle.Turtle()
    turt.penup()
    turt.speed(0)
    turt.hideturtle()
    left = grid.left - STEP // 2
    right = grid.right + STEP // 2
    top = grid.top + STEP // 2
    bottom = grid.bottom - STEP // 2
    turt.goto(left, top)
    turt.pendown()
    # Make the rows
    for i in range(height + 1):
        edge = (right, left)
        turt.goto(edge[i % 2], top - STEP * i)
        if not top - STEP * i == bottom:
            turt.goto(edge[i % 2], top - STEP * (i + 1))
    # Make the columns
    turt.goto(left, bottom)
    for i in range(width + 1):
        edge = (top, bottom)
        turt.goto(left + STEP * i, edge[i % 2])
        if not left + STEP * i == right:
            turt.goto(left + STEP * (i + 1), edge[i % 2])
    # Ensure the last edge is made.
    turt.goto(right, bottom)
    turt.penup()


def init_turt(turt: turtle.Turtle, speed_var: tk.IntVar, grid: points) -> None:
    """Put the turtle in its starting spot."""
    turt.clear()
    turt.penup()
    turt.speed(0)
    turt.hideturtle()
    turt.shape("turtle")
    # Set the turtle's starting color
    color(turt=turt)
    # Set the turtle's starting position
    turt.goto(
        random.choice((grid.left, grid.right)),
        random.choice((grid.top, grid.bottom)),
    )
    # Set the turtle's starting heading
    if turt.position()[1] == grid.top:
        turt.setheading(270)
    else:
        turt.setheading(90)
    turt.speed(5)
    speed_var.set(turt.speed())
    turt.showturtle()
    turt.pensize(3)
    turt.pendown()


def info_pane(speed_var: tk.Variable) -> tk.Toplevel:
    """Add an info pane to show commands and turtle speed."""
    pane = tk.Toplevel()
    tk.Label(pane, text="Commands:").pack()
    tk.Label(pane, text="Forward: Up Arrow").pack()
    tk.Label(pane, text="Right: Right Arrow").pack()
    tk.Label(pane, text="Left: Left Arrow").pack()
    tk.Label(pane, text="Change Color: c").pack()
    tk.Label(pane, text="Change Speed: f/s").pack()
    speed_pane = tk.Frame(pane)
    tk.Label(speed_pane, text="Speed: ").pack(side="left")
    speed = tk.Label(speed_pane, textvariable=speed_var)
    speed.pack(side="right")
    speed_pane.pack()
    tk.Label(pane, text="Reset: r").pack()
    tk.Label(pane, text="Exit: q").pack()
    return pane


def pane_position(screen: turtle.TurtleScreen, pane: tk.Toplevel) -> None:
    """Place the info pane in a reasonable spot"""
    canv = screen.getcanvas()
    screen_position_x = canv.winfo_rootx()
    screen_position_y = canv.winfo_rooty()

    pane_width = pane.winfo_reqwidth()
    loc_x = screen_position_x - 5 - pane_width
    if loc_x < 0:
        loc_x = screen_position_x + screen.window_width() + 5
    pane.geometry(f"+{loc_x}+{screen_position_y}")


def get_grid_size() -> tuple[int, int]:
    """Ask the user for the desired grid size.
    Grid size is limited to the number of cells that fit on screen.
    """

    def max_size(*_: tk.Event[tk.Entry]) -> None:
        max_width = inputs.winfo_screenwidth() // STEP - 4
        max_height = inputs.winfo_screenheight() // STEP - 4
        width.set(min(width.get(), max_width))
        height.set(min(height.get(), max_height))

    inputs = tk.Tk()
    width = tk.IntVar(inputs, value=8)
    height = tk.IntVar(inputs, value=8)
    tk.Label(inputs, text="Width:", justify="left").grid(row=0, column=0)
    tk.Label(inputs, text="Height:", justify="left").grid(row=1, column=0)
    input_width = tk.Entry(inputs, textvariable=width)
    input_width.grid(row=0, column=1)
    input_width.bind("<FocusOut>", max_size)
    input_height = tk.Entry(inputs, textvariable=height)
    input_height.grid(row=1, column=1)
    input_height.bind("<FocusOut>", max_size)
    tk.Button(inputs, text="Ok", command=inputs.destroy).grid(row=2, column=0)
    inputs.mainloop()
    return width.get(), height.get()


def main() -> None:
    """Create the screen and turtle. Add callbacks to commands for the turtle."""
    width, height = get_grid_size()
    grid = points(
        -STEP * width // 2,
        +STEP * width // 2,
        +STEP * height // 2,
        -STEP * height // 2,
    )

    screen = turtle.Screen()
    screen.setup(
        width=grid.right - grid.left + 2 * STEP,
        height=grid.top - grid.bottom + 2 * STEP,
    )
    screen.title("Isla's Turtle Game.")
    speed_var = tk.IntVar()
    turt = turtle.Turtle()
    turt.hideturtle()
    pane = info_pane(speed_var)
    pane_position(screen, pane)
    draw_grid(grid=grid, height=height, width=width)
    init_turt(turt=turt, speed_var=speed_var, grid=grid)

    screen.onkey(lambda: forward(turt=turt, grid=grid), "Up")
    screen.onkey(lambda: turn_right(turt), "Right")
    screen.onkey(lambda: turn_left(turt), "Left")
    screen.onkey(lambda: color(turt), "c")
    screen.onkey(lambda: init_turt(turt=turt, speed_var=speed_var, grid=grid), "r")
    screen.onkey(lambda: change_speed(turt, 1, speed_var), "f")
    screen.onkey(lambda: change_speed(turt, -1, speed_var), "s")
    screen.onkey(quit, "q")

    screen.listen()
    screen.mainloop()


if __name__ == "__main__":
    main()
