from dataclasses import dataclass
import itertools
import random
import textwrap
from PIL import Image, ImageDraw, ImageFont

@dataclass
class WordSpc:
    word: str
    spc: str = " "

    def __str__(self):
        return f"{self.word}{self.spc}"


def get_width(input_, target_lines):
    """Vary textwraps of INPUT from 50 to 70 by 1 to see which hit the desired
    lines with the least length variance. Assert that as soon as we hit the
    line target, we are done.
    """
    for w in range(30, 71, 1):
        raw_lines = textwrap.wrap(input_, width=w)
        if len(raw_lines) == target_lines:
            return w


def get_lines(input_, width):
    """Return a list of spaced words for the desired width"""
    raw_lines = [(x, len(x)) for x in textwrap.wrap(input_.upper(), width=width)]
    max_line = max([rl[1] for rl in raw_lines])
    lines = []
    for rl in raw_lines:
        lines.append([WordSpc(x) for x in rl[0].split()])
    for i, cur_line in enumerate(lines):
        pad_spaces = max_line - raw_lines[i][1]
        for w in zip(range(0, pad_spaces), itertools.cycle(cur_line)):
            w[1].spc += " "
    return ["".join([str(w) for w in l]) for l in lines]


def get_clues(lines):
    clues = []
    for i in range(len(lines[0])):
        clues.append([])
        for line in lines:
            clues[-1].append(line[i])
        random.shuffle(clues[-1])
    return ["".join((clue[i] for clue in clues)) for i in range(len(lines))]


def get_image(lines, clues, ref):
    w = 40
    h = 60
    extra = 1
    im = Image.new("1", (w * width + 1, 2 * h * len(lines) + extra * h + 1), (255))
    draw = ImageDraw.Draw(im)
    font  = ImageFont.truetype(font='./Courier.ttf', size=55)
    offset = 0
    for do_lines in (lines, clues):
        for iy in range(0, len(lines)):
            for ix in range(width):
                x0 = ix * w
                y0 = iy * h + offset
                if do_lines == lines:
                    c = " " if do_lines[iy][ix] == " " else ""
                else:
                    c = do_lines[iy][ix]
                draw.rectangle(
                    ((x0, y0), (x0 + w, y0 + h)), fill=(0) if c == " " else None
                )
                draw.text((x0 + 4, y0 + 4), c, font=font) #, anchor="tl")
        offset = (len(lines) + extra) * h

    im.save(f'/tmp/{ref.replace(" ","_")}.png','PNG')


if __name__ == "__main__":
    INPUT = {"Luke 24v44" : "And he said unto them, These are the words which I spake unto you, while I was yet with you, that all things must be fulfilled, which were written in the law of Moses, and in the prophets, and in the psalms, concerning me."
,"Matthew 8v27" : "But the men marvelled, saying, What manner of man is this, that even the winds and the sea obey him!"
,"John 6v47-48" : "Verily, verily, I say unto you, He that believeth on me hath everlasting life. 48 I am that bread of life."
,"John 8v12" : "Then spake Jesus again unto them, saying, I am the light of the world: he that followeth me shall not walk in darkness, but shall have the light of life."
,"John 11v25" : "Jesus said unto her, I am the resurrection, and the life: he that believeth in me, though he were dead, yet shall he live."
}
    for ref, inp in INPUT.items():
        width = get_width(f'{inp} {ref}', 4)
        lines = get_lines(f'{inp} {ref}', width)
        clues = get_clues(lines)
        get_image(lines, clues, ref)
