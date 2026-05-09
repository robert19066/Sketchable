
"""
licenced under the GNU Affero General Public License v3.0 (AGPL3)
This file is used for testing the PyDraw Library.                    
"""

"""
PyMaze — WASD maze game.
Renderer: turtle (the engine behind PyPen).

Controls
--------
  W / ↑   move up
  S / ↓   move down
  A / ←   move left
  D / →   move right
  R       new maze
  Q       quit

Requirements: Python 3 standard library only (turtle, random, sys, time).
"""

import turtle
import random
import sys
import time

sys.setrecursionlimit(10_000)


# ── Config ────────────────────────────────────────────────────────────────────

CELL   = 30          # px per grid cell
COLS   = 23          # maze width  — keep odd
ROWS   = 23          # maze height — keep odd
PAD    = 5           # player square inset from cell edge

# Palette — dark navy / neon accent
C_BG      = "#0a0a14"
C_WALL    = "#1c2b4a"
C_WALL_HI = "#243760"   # wall highlight (top/left edge)
C_PATH    = "#0a0a14"
C_EXIT    = "#f5a623"
C_EXIT_IN = "#ffd280"
C_PLAYER  = "#e94560"
C_PLAYER2 = "#ff6b82"   # player highlight
C_HUD     = "#8899bb"
C_WIN     = "#e94560"
C_STEPS   = "#4ecca3"


# ── Maze generation — iterative DFS (avoids recursion limit issues) ───────────

def make_maze(rows: int, cols: int) -> list:
    """Return a rows×cols grid.  0 = path, 1 = wall, 2 = exit."""
    grid = [[1] * cols for _ in range(rows)]

    # Iterative DFS carver
    stack = [(1, 1)]
    grid[1][1] = 0

    while stack:
        r, c = stack[-1]
        dirs = [(0, 2), (2, 0), (0, -2), (-2, 0)]
        random.shuffle(dirs)
        moved = False
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 0 < nr < rows - 1 and 0 < nc < cols - 1 and grid[nr][nc] == 1:
                grid[r + dr // 2][c + dc // 2] = 0
                grid[nr][nc] = 0
                stack.append((nr, nc))
                moved = True
                break
        if not moved:
            stack.pop()

    grid[rows - 2][cols - 2] = 2   # exit marker
    return grid


# ── World-coordinate helpers ──────────────────────────────────────────────────

def _origin(cols, rows):
    return -(cols * CELL) // 2, (rows * CELL) // 2

def cell_to_world(row: int, col: int, cols: int, rows: int):
    """Bottom-left corner of a grid cell in turtle world coords."""
    ox, oy = _origin(cols, rows)
    return ox + col * CELL, oy - (row + 1) * CELL


def fill_rect(t: turtle.Turtle, x, y, w, h, color):
    t.penup()
    t.goto(x, y)
    t.fillcolor(color)
    t.begin_fill()
    for side in (w, h, w, h):
        t.forward(side)
        t.left(90)
    t.end_fill()


# ── Game state ────────────────────────────────────────────────────────────────

class Game:
    def __init__(self):
        self.maze: list   = []
        self.pr:   int    = 1      # player row
        self.pc:   int    = 1      # player col
        self.steps: int   = 0
        self.won:  bool   = False
        self.start_time   = time.time()

    def reset(self):
        self.maze       = make_maze(ROWS, COLS)
        self.pr, self.pc = 1, 1
        self.steps       = 0
        self.won         = False
        self.start_time  = time.time()


# ── Rendering ─────────────────────────────────────────────────────────────────

def draw_maze(t: turtle.Turtle, g: Game):
    t.clear()
    t.speed(0)
    t.penup()
    for r in range(ROWS):
        for c in range(COLS):
            x, y = cell_to_world(r, c, COLS, ROWS)
            v = g.maze[r][c]
            if v == 1:
                # main wall body
                fill_rect(t, x, y, CELL, CELL, C_WALL)
                # subtle top highlight for pseudo-3D feel
                t.penup(); t.goto(x, y + CELL)
                t.pencolor(C_WALL_HI); t.pendown()
                t.goto(x + CELL, y + CELL)
                t.penup()
            elif v == 2:
                fill_rect(t, x, y, CELL, CELL, C_EXIT)
                # inner glow square
                pad = 6
                fill_rect(t, x + pad, y + pad,
                          CELL - pad * 2, CELL - pad * 2, C_EXIT_IN)


def draw_player(t: turtle.Turtle, g: Game):
    t.clear()
    t.speed(0)
    t.penup()
    x, y = cell_to_world(g.pr, g.pc, COLS, ROWS)
    # shadow
    fill_rect(t, x + PAD + 2, y + PAD - 2,
              CELL - PAD * 2, CELL - PAD * 2, "#3a0010")
    # body
    fill_rect(t, x + PAD, y + PAD,
              CELL - PAD * 2, CELL - PAD * 2, C_PLAYER)
    # top-left highlight
    hi = 4
    fill_rect(t, x + PAD, y + CELL - PAD - hi,
              hi * 2, hi, C_PLAYER2)
    fill_rect(t, x + PAD, y + PAD,
              hi, CELL - PAD * 2 - hi, C_PLAYER2)


def draw_hud(t: turtle.Turtle, g: Game):
    t.clear()
    t.penup()
    ox, oy = _origin(COLS, ROWS)
    t.goto(ox, oy + 18)
    t.color(C_HUD)
    elapsed = int(time.time() - g.start_time)
    t.write(
        f"  steps: {g.steps:04d}    time: {elapsed:03d}s    [R] new maze   [Q] quit",
        font=("Courier", 10, "normal")
    )


def draw_win(t: turtle.Turtle, g: Game):
    t.clear()
    elapsed = int(time.time() - g.start_time)
    t.penup()

    # dim overlay — draw a big filled rect
    t.goto(-COLS * CELL // 2, -ROWS * CELL // 2)
    t.fillcolor("#0a0a1499")   # semi-transparent isn't supported in turtle,
    # so we layer text over instead:

    t.color(C_WIN)
    t.goto(0, 40)
    t.write("YOU ESCAPED!", align="center", font=("Courier", 32, "bold"))

    t.color(C_STEPS)
    t.goto(0, -2)
    t.write(f"steps: {g.steps}   time: {elapsed}s",
            align="center", font=("Courier", 16, "normal"))

    t.color(C_HUD)
    t.goto(0, -38)
    t.write("press  R  to try a new maze",
            align="center", font=("Courier", 12, "normal"))


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    sc = turtle.Screen()
    sc.title("PyMaze")
    sc.bgcolor(C_BG)
    sc.setup(COLS * CELL + 60, ROWS * CELL + 60)
    sc.tracer(0)

    # Three turtles so maze isn't redrawn every frame
    maze_t   = turtle.Turtle(); maze_t.hideturtle()
    player_t = turtle.Turtle(); player_t.hideturtle()
    hud_t    = turtle.Turtle(); hud_t.hideturtle()
    win_t    = turtle.Turtle(); win_t.hideturtle()

    g = Game()
    g.reset()

    def refresh(redraw_maze=False):
        if redraw_maze:
            draw_maze(maze_t, g)
        draw_player(player_t, g)
        draw_hud(hud_t, g)
        sc.update()

    def move(dr: int, dc: int):
        if g.won:
            return
        nr, nc = g.pr + dr, g.pc + dc
        if 0 <= nr < ROWS and 0 <= nc < COLS and g.maze[nr][nc] != 1:
            g.pr, g.pc = nr, nc
            g.steps += 1
            if g.maze[nr][nc] == 2:
                g.won = True
                refresh()
                draw_win(win_t, g)
                sc.update()
                return
        refresh()

    def restart():
        win_t.clear()
        g.reset()
        refresh(redraw_maze=True)

    def quit_game():
        sc.bye()

    sc.listen()
    # WASD
    sc.onkeypress(lambda: move(-1,  0), "w")
    sc.onkeypress(lambda: move( 1,  0), "s")
    sc.onkeypress(lambda: move( 0, -1), "a")
    sc.onkeypress(lambda: move( 0,  1), "d")
    # Arrow keys
    sc.onkeypress(lambda: move(-1,  0), "Up")
    sc.onkeypress(lambda: move( 1,  0), "Down")
    sc.onkeypress(lambda: move( 0, -1), "Left")
    sc.onkeypress(lambda: move( 0,  1), "Right")
    # Meta
    sc.onkeypress(restart,   "r")
    sc.onkeypress(quit_game, "q")

    # HUD timer — updates every second even when player isn't moving
    def tick():
        if not g.won:
            draw_hud(hud_t, g)
            sc.update()
        sc.ontimer(tick, 1000)

    refresh(redraw_maze=True)
    tick()
    turtle.mainloop()


if __name__ == "__main__":
    main()