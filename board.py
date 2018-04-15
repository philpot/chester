from __future__ import print_function

import sys

FILES = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
RANKS = range(1, 9)

def fval(f):
    return {'a': 0,
            'b': 1,
            'c': 2,
            'd': 3,
            'e': 4,
            'f': 5,
            'g': 6,
            'h': 7}[f]

def signum(x):
    return (x > 0) - (x < 0)

def ranks(src, dest):
    assert (1 <= src) and (src <= 8)
    assert (1 <= dest) and (dest <= 8)
    s = signum(dest - src)
    if s == 0:
        return [src]
    else:
        return range(src, dest+s, s)

def files(src, dest):
    fidx = FILES.index(src)
    tidx = FILES.index(dest)
    if fidx <= tidx:
        return FILES[fidx:1+tidx]
    else:
        return FILES[fidx:tidx-1:-1]

class Piece(object):
    name = 'X'
    chars = {"W": u'\u263A',
             "B": u'\u263B'}

    def __init__(self, f=None, r=None, color="W"):
        self.f = f
        self.r = r
        self.color = color
        if self.color == 'W':
            self.up = 1
        else:
            self.up = -1
        if self.color == 'W':
            self.home = 1
        else:
            self.home = 8
        self.start = self.home

    @property
    def fv(self):
        return fval(self.f)

    def char(self):
        return self.__class__.chars[self.color]

    def __unicode__(self):
        return (u"{name} @{f}{r}"
                .format(name=self.__class__.chars[self.color],
                        # color=self.color,
                        f=self.f,
                        r=self.r))

    def __repr__(self):
        return self.__unicode__().encode('utf-8')


DARK = u'\u2593'


# ♔	9812	♔	2654	 	WHITE CHESS KING
# ♕	9813	♕	2655	 	WHITE CHESS QUEEN
# ♖	9814	♖	2656	 	WHITE CHESS ROOK
# ♗	9815	♗	2657	 	WHITE CHESS BISHOP
# ♘	9816	♘	2658	 	WHITE CHESS KNIGHT
# ♙	9817	♙	2659	 	WHITE CHESS PAWN
# ♚	9818	♚	265A	 	BLACK CHESS KING
# ♛	9819	♛	265B	 	BLACK CHESS QUEEN
# ♜	9820	♜	265C	 	BLACK CHESS ROOK
# ♝	9821	♝	265D	 	BLACK CHESS BISHOP
# ♞	9822	♞	265E	 	BLACK CHESS KNIGHT
# ♟	9823	♟	265F	 	BLACK CHESS PAWN


class King(Piece):
    name = 'K'
    chars = {"W": u'\u2654',
             "B": u'\u265A'}

    def canmove(self, board, f, r):
        if 1 <= r and r <= 8 and f in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']:
            pass
        else:
            return False
        fv = fval(f)
        if abs(self.r - r) <= 1  and abs(self.fv - fv) <= 1:
            if (board.bref(f, r) is None
                or board.bref(f, r).color != self.color):
                return True
            else:
                return False
        if abs(self.r - r) == 1 and abs(self.fv - fv) == 2:
            if (board.bref(f, r) is None
                or board.bref(f, r).color != self.color):
                return True
            else:
                return False
        return False


class Queen(Piece):
    name = 'Q'
    chars = {"W": u'\u2655',
             "B": u'\u265B'}

class Rook(Piece):
    name = 'R'
    chars = {"W": u'\u2656',
             "B": u'\u265C'}

    def canmove(self, board, f, r):
        up = self.up
        start = self.start
        if f not in FILES:
            return False
        if r not in RANKS:
            return False
        if self.f == f and self.r == r:
            return False
        fv = fval(f)
        if self.r == r and self.f != f:
            # Move along file
            for k in files(self.f, f)[1:-1]:
                if board.bref(k, r):
                    # something in the way
                    return False
            target = board.bref(f, r)
            if target is None:
                return True
            else:
                if target.color == self.color:
                    return False
                else:
                    # capture
                    return target
        elif self.f == f and self.r != r:
            # Move along rank
            for k in ranks(self.r, r)[1:-1]:
                if board.bref(f, k):
                    # something in the way
                    return False
            target = board.bref(f, r)
            if target is None:
                return True
            else:
                if target.color == self.color:
                    return False
                else:
                    # capture
                    return target
        return False

class Bishop(Piece):
    name = 'B'
    chars = {"W": u'\u2657',
             "B": u'\u265D'}

    def canmove(self, board, f, r):
        up = self.up
        start = self.start
        if f not in FILES:
            return False
        if r not in RANKS:
            return False
        if self.f == f and self.r == r:
            return False
        fv = fval(f)
        if abs(self.fv - fv) != abs(self.r - r):
            return False
        # Move along file and rank simultaneously
        df = signum(fv - self.fv)
        dr = signum(r - self.r)
        rs = RANKS[self.r:r:dr]
        fs = FILES[self.fv+df:fv+df:df]
        print("Ranks {rs} files {fs}"
              .format(rs=rs, fs=fs))
        for (j, k) in zip(fs[:-1], rs[:-1]):
            if board.bref(j, k):
                return False
        target = board.bref(f, r)
        if target is None:
            return True
        else:
            if target.color == self.color:
                return False
            else:
                # capture
                return target
        return False


class Knight(Piece):
    name = 'N'
    chars = {"W": u'\u2658',
             "B": u'\u265E'}

    def canmove(self, board, f, r):
        up = self.up
        start = self.start
        if f not in FILES:
            return False
        if r not in RANKS:
            return False
        if self.f == f and self.r == r:
            return False
        fv = fval(f)
        if (abs(self.r - r) == 2 and abs(self.fv - fv) == 1
            or
            abs(self.r - r) == 1 and abs(self.fv - fv) == 2):
            # then
            target = board.bref(f, r)
            if target is None:
                return True
            else:
                if target.color == self.color:
                    return False
                else:
                    # capture
                    return target
        return False


class Pawn(Piece):
    name = '_'
    chars = {"W": u'\u2659',
             "B": u'\u265F'}

    def __init__(self, **kwargs):
        super(Pawn, self).__init__(**kwargs)
        self.start = self.home + self.up

    def canmove(self, board, f, r):
        up = self.up
        start = self.start
        if f not in FILES:
            return False
        if r not in RANKS:
            return False
        if self.f == f and self.r == r:
            return False
        fv = fval(f)
        # From starting rank: may move 1 or two ranks
        if self.r == start:
            if (self.f == f
                and (r == start + 2*up)
                and board.bref(f, start+up) is None
                and board.bref(f, start+2*up) is None):
                # then
                return True
        # May always move one rank ahead
        if self.f == f and (r == start + up):
            if (self.f == f
                and (r == start + up)
                and board.bref(f, start+up) is None):
                # then
                return True
        # Capture
        if (abs(self.fv - fv) == 1
            and (r == start + up)
            and board.bref(f, start+up) is not None
            and board.bref(f, start+up).color != self.color):
            # capture
            return board.bref(f, start+up)
        # Otherwise, no
        return False


class Board(object):
    def __init__(self):
        self.b = [[None for _ in range(8)] for _ in range(8)]
        self.setup()

    def bref(self, f, r):
        y = r - 1
        x = ord(f) - ord('a')
        return self.b[y][x]

    def setbref(self, f, r, p):
        y = r - 1
        x = ord(f) - ord('a')
        self.b[y][x] = p
        return p

    def setup(self):
        self.setbref('a', 1, Rook(f='a', r=1, color='W'))
        self.setbref('b', 1, Knight(f='b', r=1, color='W'))
        self.setbref('c', 1, Bishop(f='c', r=1, color='W'))
        self.setbref('d', 1, Queen(f='d', r=1, color='W'))
        self.setbref('e', 1, King(f='e', r=1, color='W'))
        self.setbref('f', 1, Bishop(f='f', r=1, color='W'))
        self.setbref('g', 1, Knight(f='g', r=1, color='W'))
        self.setbref('h', 1, Rook(f='h', r=1, color='W'))

        self.setbref('a', 2, Pawn(f='a', r=2, color='W'))
        self.setbref('b', 2, Pawn(f='b', r=2, color='W'))
        self.setbref('c', 2, Pawn(f='c', r=2, color='W'))
        self.setbref('d', 2, Pawn(f='d', r=2, color='W'))
        self.setbref('e', 2, Pawn(f='e', r=2, color='W'))
        self.setbref('f', 2, Pawn(f='f', r=2, color='W'))
        self.setbref('g', 2, Pawn(f='g', r=2, color='W'))
        self.setbref('h', 2, Pawn(f='h', r=2, color='W'))

        self.setbref('a', 7, Pawn(f='a', r=7, color='B'))
        self.setbref('b', 7, Pawn(f='b', r=7, color='B'))
        self.setbref('c', 7, Pawn(f='c', r=7, color='B'))
        self.setbref('d', 7, Pawn(f='d', r=7, color='B'))
        self.setbref('e', 7, Pawn(f='e', r=7, color='B'))
        self.setbref('f', 7, Pawn(f='f', r=7, color='B'))
        self.setbref('g', 7, Pawn(f='g', r=7, color='B'))
        self.setbref('h', 7, Pawn(f='h', r=7, color='B'))

        self.setbref('a', 8, Rook(f='a', r=8, color='B'))
        self.setbref('b', 8, Knight(f='b', r=8, color='B'))
        self.setbref('c', 8, Bishop(f='c', r=8, color='B'))
        self.setbref('d', 8, Queen(f='d', r=8, color='B'))
        self.setbref('e', 8, King(f='e', r=8, color='B'))
        self.setbref('f', 8, Bishop(f='f', r=8, color='B'))
        self.setbref('g', 8, Knight(f='g', r=8, color='B'))
        self.setbref('h', 8, Rook(f='h', r=8, color='B'))

    def show(self):
        print('    a   b   c   d   e   f   g   h')
        print('  +---+---+---+---+---+---+---+---+')
        for y in range(7, -1, -1):
            rank = self.b[y]
            print("{r} |".format(r=y+1), end="")
            for (x, cell) in enumerate(rank):
                space = ' ' if (x + y) % 2 else DARK
                space = ' '
                if cell:
                    print(space + cell.char() + space + '|', end="")
                else:
                    print(space + space + space + '|', end="")
            print(" {r}".format(r=y+1))
            print('  +---+---+---+---+---+---+---+---+')
        print('    a   b   c   d   e   f   g   h  ')



    def find_piece(self, datatype, color, f=None, r=None):
        if isinstance(datatype, basestring):
            datatype = PIECECODES[datatype]
        pieces = []
        for rank in self.b:
            for piece in rank:
                if piece and isinstance(piece, datatype) and piece.color == color:
                    if f and (f != piece.f):
                        continue
                    if r and (r != piece.r):
                        continue
                    pieces.append(piece)
        if len(pieces) == 0:
            raise ValueError
        elif len(pieces) == 1:
            return pieces
        else:
            print("More than one")
            return pieces

    def move(self, piece, f, r):
        "assumes move is legal, no checking"
        f0 = piece.f
        r0 = piece.r
        self.setbref(f, r, piece)
        self.setbref(f0, r0, None)
        piece.f = f
        piece.r = r
        return piece

    def test(self):
        BQ = self.bref('d', 8)
        self.move(BQ, 'c', 3)
        WRL = self.bref('a', 1)
        self.move(WRL, 'a', 3)
        self.show()


class Command(object):
    pass


PIECECODES = {"Q": Queen,
              'K': King,
              "R": Rook,
              "B": Bishop,
              "N": Knight,
              "_": Pawn}


def cmd(b, s, color='W'):
    (p, f, r) = s
    r = int(r)
    datatype = PIECECODES[p]
    print(datatype, color, f, r)
    cands = []
    for p in b.find_piece(datatype, color):
        result = p.canmove(b, f, r)
        if result:
            cands.append((p, result))
    if len(cands) > 1:
        print("ambiguous")
    elif len(cands) == 0:
        print("No such legal move")
    else:
        (p, result) = cands[0]
        former = str(p)
        b.move(p, f, r)
        if result is True:
            print("{piece} moves to {f}{r}"
                  .format(piece=p,
                          f=f,
                          r=r))
        else:
            print("{piece} takes {target} at {f}{r}"
                  .format(piece=former,
                          target=result,
                          f=f,
                          r=r))
