import random
import tkinter as tk
import turtle
from typing import NamedTuple

points = NamedTuple(
    "points", [("left", int), ("right", int), ("top", int), ("bottom", int)]
)
STEP = 50
GRID_WIDTH = 8
GRID_HEIGHT = 8
BOUNDARIES = points(
    -STEP * GRID_WIDTH // 2,
    +STEP * GRID_WIDTH // 2,
    +STEP * GRID_HEIGHT // 2,
    -STEP * GRID_HEIGHT // 2,
)


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
    heading_complex = 1j ** heading_quadrant  # j**0 == 1+0j, j**1 == 0+1j
    x = int(heading_complex.real)
    y = int(heading_complex.imag)
    return (x, y)


def forward(turt: turtle.Turtle) -> None:
    """Move forward if possible"""
    current_x, current_y = turt.position()
    heading_x, heading_y = get_heading(turt)
    new_x = round(current_x) + heading_x * STEP
    new_y = round(current_y) + heading_y * STEP
    if (
        not BOUNDARIES.left <= new_x <= BOUNDARIES.right
        or not BOUNDARIES.bottom <= new_y <= BOUNDARIES.top
    ):
        return
    # re-adjust to be on grid.
    turt.goto(new_x, new_y)


def right(turt: turtle.Turtle) -> None:
    """Turn right 90 degrees"""
    turt.right(90)


def left(turt: turtle.Turtle) -> None:
    """Turn left 90 degrees"""
    turt.left(90)


def change_speed(turt: turtle.Turtle, delta: int, speed_var: tk.Variable) -> None:
    """Change the turtle speed in range 1, 10 inclusive"""
    current = turt.speed()
    new = current + delta
    if not 1 <= new <= 10:
        return
    turt.speed(new)
    speed_var.set(turt.speed())


def draw_grid(turt: turtle.Turtle) -> None:
    """Draw the initial grid."""
    turt.penup()
    turt.speed(0)
    turt.hideturtle()
    left = BOUNDARIES.left - STEP // 2
    right = BOUNDARIES.right + STEP // 2
    top = BOUNDARIES.top + STEP // 2
    bottom = BOUNDARIES.bottom - STEP // 2
    turt.goto(left, top)
    turt.pendown()
    # Make the rows
    for i in range(GRID_HEIGHT + 1):
        edge = (right, left)
        turt.goto(edge[i % 2], top - STEP * i)
        if not top - STEP * i == bottom:
            turt.goto(edge[i % 2], top - STEP * (i + 1))
    # Make the columns
    turt.goto(left, bottom)
    for i in range(GRID_WIDTH + 1):
        edge = (top, bottom)
        turt.goto(left + STEP * i, edge[i % 2])
        if not left + STEP * i == right:
            turt.goto(left + STEP * (i + 1), edge[i % 2])
    # Ensure the last edge is made.
    turt.goto(right, bottom)
    turt.penup()


def init_turt(turt: turtle.Turtle) -> turtle.Turtle:
    """Put the turtle in its starting spot."""
    turt.penup()
    turt.speed(0)
    turt.hideturtle()
    turt.shape("turtle")
    # Set the turtle's starting color
    color(turt=turt)
    # Set the turtle's starting position
    turt.goto(
        random.randint(-GRID_WIDTH // 2, GRID_WIDTH // 2) * STEP,
        random.randint(-GRID_HEIGHT // 2, GRID_HEIGHT // 2) * STEP,
    )
    # Set the turtle's starting heading
    turt.right(random.choice((0, 90, 180, 270)))
    turt.speed(5)
    turt.showturtle()
    turt.pendown()
    return turt


def info_pane(turt: turtle.Turtle, speed_var: tk.Variable) -> tk.Toplevel:
    pane = tk.Toplevel()
    tk.Label(pane, text="Commands:").pack()
    tk.Label(pane, text="Forward: Up Arrow").pack()
    tk.Label(pane, text="Right: Right Arrow").pack()
    tk.Label(pane, text="Left: Left Arrow").pack()
    tk.Label(pane, text="Color: c").pack()
    tk.Label(pane, text="Change Speed: f/s").pack()
    tk.Label(pane, text="Exit: q").pack()
    speed_pane = tk.Frame(pane)
    tk.Label(speed_pane, text="Speed: ").pack(side="left")
    speed = tk.Label(speed_pane, textvariable=speed_var)
    speed.pack(side="right")
    speed_pane.pack()
    return pane


def pane_position(screen: turtle.TurtleScreen, pane: tk.Toplevel) -> None:
    canv = screen.getcanvas()
    screen_position_x = canv.winfo_rootx()
    screen_position_y = canv.winfo_rooty()

    pane_width = pane.winfo_reqwidth()
    loc_x = screen_position_x - 5 - pane_width
    if loc_x < 0:
        loc_x = screen_position_x + screen.window_width() + 5
    pane.geometry(f"+{loc_x}+{screen_position_y}")


def main() -> None:
    """Create the screen and turtle. Add callbacks to commands for the turtle."""
    screen = turtle.Screen()
    screen.setup(
        width=BOUNDARIES.right - BOUNDARIES.left + 2 * STEP,
        height=BOUNDARIES.top - BOUNDARIES.bottom + 2 * STEP,
    )
    screen.title("Isla's Turtle Game.")
    turt = turtle.Turtle()
    speed_var = tk.IntVar()
    pane = info_pane(turt, speed_var)
    pane_position(screen, pane)
    draw_grid(turt)
    init_turt(turt)
    speed_var.set(turt.speed())

    screen.onkey(lambda: forward(turt), "Up")
    screen.onkey(lambda: right(turt), "Right")
    screen.onkey(lambda: left(turt), "Left")
    screen.onkey(lambda: color(turt), "c")
    screen.onkey(lambda: change_speed(turt, 1, speed_var), "f")
    screen.onkey(lambda: change_speed(turt, -1, speed_var), "s")
    screen.onkey(quit, "q")

    screen.listen()
    screen.mainloop()


if __name__ == "__main__":
    main()
