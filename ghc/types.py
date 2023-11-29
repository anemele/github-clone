from typing import Generator, Union

Ls_Gs = Union[list[str], Generator[str, None, None]]
G_Ts = Generator[tuple[str, str], None, None]
