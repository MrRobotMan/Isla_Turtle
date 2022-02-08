import random
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
    STEP * GRID_WIDTH // 2,
    STEP * GRID_HEIGHT // 2,
    -STEP * GRID_HEIGHT // 2,
)


def quit() -> None:
    turtle.bye()


def color(turt: turtle.Turtle) -> None:
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
    turt.right(90)


def left(turt: turtle.Turtle) -> None:
    turt.left(90)


def change_speed(turt: turtle.Turtle, delta: int) -> None:
    current = turt.speed()
    new = current + delta
    if not 1 <= new <= 10:
        return
    turt.speed(new)


def draw_grid(turt: turtle.Turtle) -> None:
    """Draw the initial grid."""
    turt.penup()
    top = BOUNDARIES.top + STEP // 2
    bottom = BOUNDARIES.bottom - STEP // 2
    left = BOUNDARIES.left - STEP // 2
    right = BOUNDARIES.right + STEP // 2
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
    turt.goto(right, bottom)
    turt.penup()


def init_turt() -> turtle.Turtle:
    turt = turtle.Turtle()
    turt.penup()
    turt.speed(0)
    turt.hideturtle()
    draw_grid(turt)
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


def main() -> None:
    screen = turtle.Screen()
    screen.setup(
        width=BOUNDARIES.right - BOUNDARIES.left + 2 * STEP,
        height=BOUNDARIES.top - BOUNDARIES.bottom + 2 * STEP,
    )
    screen.title("Isla's Turtle Game.")
    turt = init_turt()

    screen.onkey(lambda: forward(turt), "Up")
    screen.onkey(lambda: right(turt), "Right")
    screen.onkey(lambda: left(turt), "Left")
    screen.onkey(lambda: color(turt), "c")
    screen.onkey(lambda: change_speed(turt, 1), "f")
    screen.onkey(lambda: change_speed(turt, -1), "s")
    screen.onkey(quit, "q")

    screen.listen()
    screen.mainloop()


if __name__ == "__main__":
    main()
