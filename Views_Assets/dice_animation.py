import random
from pathlib import Path
from typing import Optional, Tuple

import pygame


TILE_SIZE = 16  # this sheet is 16x16 tiles


def ease_out_cubic(t: float) -> float:
    """t in [0..1] -> eased in [0..1] (fast at start, slow at end)."""
    t = max(0.0, min(1.0, t))
    return 1 - (1 - t) ** 3


def get_tile(sheet: pygame.Surface, col: int, row: int, tile_size: int = TILE_SIZE) -> pygame.Surface:
    rect = pygame.Rect(col * tile_size, row * tile_size, tile_size, tile_size)
    return sheet.subsurface(rect).copy()


class SpriteDiceRoller:
    """
    Dice roller that uses a sprite sheet with 16x16 tiles.

    Sheet layout assumption:
      - columns: faces 1..6 (col 0..5)
      - rows: different styles/colors (row 0..N-1)
    Typical usage:
      - Use bottom row (anim_row) while rolling
      - Use top row (final_row) for the final face

    Call order:
      - dice.start() to begin
      - dice.update(dt_ms) each frame
      - dice.render() each frame
      - dice.get_result() after finished (returns int or None)
    """

    _sheet_cache: dict[str, pygame.Surface] = {}

    def __init__(
        self,
        screen: pygame.Surface,
        pos: Tuple[int, int] = (0, 0),
        scale: int = 6,
        sides: int = 6,
        duration_ms: int = 1200,
        min_interval_ms: int = 35,
        max_interval_ms: int = 220,
        anim_row: Optional[int] = None,  # if None -> bottom row
        final_row: int = 0,              # top row
        allow_repeat: bool = True,
        sound_enabled: bool = False,
        tick_sound_path: Optional[str] = None,
        end_sound_path: Optional[str] = None,
        sheet_rel_path: Tuple[str, ...] = ("Assets", "Sprites", "six_sided_die.png"),
    ):
        self.screen = screen
        self.pos = pos
        self.scale = scale
        self.sides = sides

        self.duration_ms = duration_ms
        self.min_interval_ms = min_interval_ms
        self.max_interval_ms = max_interval_ms

        self.final_row = final_row
        self.allow_repeat = allow_repeat

        # --- Load sprite sheet ONCE (class cache) ---
        base_dir = Path(__file__).resolve().parent
        sheet_path = base_dir.joinpath(*sheet_rel_path).resolve()
        key = str(sheet_path)

        if key not in SpriteDiceRoller._sheet_cache:
            SpriteDiceRoller._sheet_cache[key] = pygame.image.load(key).convert_alpha()

        self.sheet = SpriteDiceRoller._sheet_cache[key]

        # Determine rows dynamically from the image
        self.rows = self.sheet.get_height() // TILE_SIZE
        self.cols = self.sheet.get_width() // TILE_SIZE

        # If anim_row not specified, default to bottom row
        self.anim_row = (self.rows - 1) if anim_row is None else anim_row

        # Clamp safety
        self.anim_row = max(0, min(self.rows - 1, self.anim_row))
        self.final_row = max(0, min(self.rows - 1, self.final_row))

        # --- Sounds (optional) ---
        self.sound_enabled = sound_enabled
        self.tick_sound = None
        self.end_sound = None

        if self.sound_enabled:
            if tick_sound_path:
                self.tick_sound = pygame.mixer.Sound(tick_sound_path)
            if end_sound_path:
                self.end_sound = pygame.mixer.Sound(end_sound_path)

        # --- State ---
        self.is_rolling = False
        self.is_finished = False
        self.elapsed_ms = 0
        self.next_switch_in_ms = 0

        self.face = random.randint(1, self.sides)
        self.final_face: Optional[int] = None

    def start(self, forced_result: Optional[int] = None) -> None:
        """Begin rolling. Optionally force a final result (1..sides)."""
        if forced_result is not None:
            forced_result = max(1, min(self.sides, forced_result))

        self.is_rolling = True
        self.is_finished = False
        self.elapsed_ms = 0
        self.final_face = forced_result
        self._schedule_next_switch()

    def cancel(self) -> None:
        """Stop immediately; keep current face."""
        self.is_rolling = False
        self.is_finished = True
        self.final_face = self.face

    def get_result(self) -> Optional[int]:
        """Returns final dice result if finished, else None."""
        return self.final_face if self.is_finished else None

    def update(self, dt_ms: int) -> None:
        """Advance animation by dt in milliseconds."""
        if not self.is_rolling or self.is_finished:
            return

        self.elapsed_ms += dt_ms

        # Finish roll
        if self.elapsed_ms >= self.duration_ms:
            self.is_rolling = False
            self.is_finished = True

            if self.final_face is None:
                self.final_face = random.randint(1, self.sides)

            self.face = self.final_face

            if self.sound_enabled and self.end_sound:
                self.end_sound.play()

            return

        # Switch faces when timer hits 0
        self.next_switch_in_ms -= dt_ms
        if self.next_switch_in_ms <= 0:
            self._change_face()
            self._schedule_next_switch()

    def render(self) -> None:
        """Draw current face using anim_row while rolling, final_row otherwise."""
        col = max(0, min(self.cols - 1, self.face - 1))
        row = self.anim_row if (self.is_rolling and not self.is_finished) else self.final_row

        tile = get_tile(self.sheet, col, row)
        size = (TILE_SIZE * self.scale, TILE_SIZE * self.scale)
        tile_big = pygame.transform.scale(tile, size)

        self.screen.blit(tile_big, self.pos)

    # ---------------- internals ----------------

    def _schedule_next_switch(self) -> None:
        t = self.elapsed_ms / max(1, self.duration_ms)  # 0..1
        eased = ease_out_cubic(t)                       # 0..1 (fast -> slow)
        interval = self.min_interval_ms + (self.max_interval_ms - self.min_interval_ms) * eased
        self.next_switch_in_ms = int(interval)

    def _change_face(self) -> None:
        old = self.face

        if self.allow_repeat or self.sides <= 1:
            self.face = random.randint(1, self.sides)
        else:
            new_val = old
            while new_val == old:
                new_val = random.randint(1, self.sides)
            self.face = new_val

        if self.sound_enabled and self.tick_sound:
            self.tick_sound.play()
