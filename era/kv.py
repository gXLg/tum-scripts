from PIL import Image, ImageDraw

class Vorlage:
  def __init__(self, c, l, crules, lrules):
    self.c = c
    self.l = l
    self.cr = { a: [i - 1 for i in b] for a, b in crules }
    self.lr = { a: [i - 1 for i in b] for a, b in lrules }

  def createKV(self, mark):
    c, l = self.c, self.l
    if mark in self.cr:
      return KV([[x in self.cr[mark] for x in range(c)] for y in range(self.l)])
    else:
      return KV([[y in self.lr[mark] for x in range(c)] for y in range(l)])


class KV:
  def __init__(self, data):
    self.data = data

  def unop(self, op):
    return KV([[op(c) for c in r] for r in self.data])
  def binop(self, op, kv):
    return KV([[op(c1, c2) for c1, c2 in zip(r1, r2)] for r1, r2 in zip(self.data, kv.data)])

  def print(self):
    for r in self.data:
      print(*["#" if c else "." for c in r])

  def draw(self, vl):
    c, l, cr, lr = vl.c, vl.l, vl.cr, vl.lr

    img = Image.new("RGB", ((c + 2) * 50, (l + 3) * 50), "white")
    draw = ImageDraw.Draw(img)

    a, b = 25, l * 50 + 25
    for i in range(c + 1):
      f = i * 50 + 25
      draw.line((f, a, f, b), "black", 2)

    b = c * 50 + 25
    for i in range(l + 1):
      f = i * 50 + 25
      draw.line((a, f, b, f), "black", 2)

    cc = [[1 for _ in range(c)] for _ in cr]
    ll = [[1 for _ in range(l)] for _ in lr]

    colors = ["blue", "red", "orange", "green", "violet", "turquoise"]
    table = { }

    for a in cr:
      if a in table:
        col = table[a]
      else:
        col = colors.pop(0)
        table[a] = col

      b = cr[a]
      m = [[i[j] for j in b] for i in cc]
      for i, r in enumerate(m):
        if all(r):
          for j in b: cc[i][j] = 0
          break
      f = l * 50 + 29 + i * 5
      for j in b:
        draw.line((25 + j * 50, f, 75 + j * 50, f), col, 4)

    for a in lr:
      if a in table:
        col = table[a]
      else:
        col = colors.pop(0)
        table[a] = col

      b = lr[a]
      m = [[i[j] for j in b] for i in ll]
      for i, r in enumerate(m):
        if all(r):
          for j in b: ll[i][j] = 0
          break
      f = c * 50 + 29 + i * 5
      for j in b:
        draw.line((f, 25 + j * 50, f, 75 + j * 50), col, 4)

    # legend
    i = 0
    a = 95 + l * 50
    for j in table:
      col = table[j]
      draw.rectangle((25 + i * 50, a, 35 + i * 50, a + 10), col)
      draw.text((40 + i * 50, a), f" {j} ", "black")
      i += 1

    # fill
    for rr, r in enumerate(self.data):
      for cc, c in enumerate(r):
        if c:
          draw.rectangle((28 + cc * 50, 28 + rr * 50, 73 + cc * 50, 73 + rr * 50), "gray")

    return img


def parse_vorlage(s):
  a, b = s.split(":")
  c, l = map(int, a.split())
  e, f = b.split("|")
  cr = []
  for i in e.split(","):
    a, *b = i.split()
    cr.append((a, [*map(int, b)]))
  lr = []
  for i in f.split(","):
    a, *b = i.split()
    lr.append((a, [*map(int, b)]))
  return Vorlage(c, l, cr, lr)

def parse_logik(s, d = True):
  tokens = []
  if d:
    look = {
      "(": "LBR",
      ")": "RBR",
      "∨": "OR",
      "∧": "AND",
      "¬": "NOT",
      **{ chr(i): "CHR" for i in range(97, 123) }
    }
  else:
    look = {
      "(": "LBR",
      ")": "RBR",
      "v": "OR",
      "^": "AND",
      "!": "NOT",
      **{ chr(i): "CHR" for i in range(65, 91) }
    }
  for i in s:
    if i in look:
      tokens.append((i, look[i]))
  tokens.append((None, "END"))

  class Tree:
    def __init__(self, left, token, right):
      self.l = left or ""
      self.t = token
      self.r = right or ""

    def __repr__(self):
      return f"[\n{self.l} {self.t} {self.r}\n]"

    def execute(self, vorlage):
      if self.t[1] == "CHR":
        return vorlage.createKV(self.t[0])
      elif self.t[1] == "NOT":
        return self.r.execute(vorlage).unop(lambda a: not a)
      elif self.t[1] == "AND":
        return self.l.execute(vorlage).binop(lambda a, b: a and b, self.r.execute(vorlage))
      elif self.t[1] == "OR":
        return self.l.execute(vorlage).binop(lambda a, b: a or b, self.r.execute(vorlage))

  class Parser:
    def __init__(self, tokens):
      self.current = None
      self.tokens = tokens
      self.n()

    def n(self):
      self.current = self.tokens.pop(0)

    def parse(self):
      if self.current[1] == "END": return None
      res = self._or()
      if self.current[1] != "END":
        raise Exception(f"Not fully parsed: {self.current}")
      return res

    def _or(self):
      res = self._and()
      while self.current[1] != "END" and self.current[1] == "OR":
        token = self.current
        self.n()
        res = Tree(res, token, self._and())
      return res

    def _and(self):
      res = self._factor()
      while self.current[1] != "END" and self.current[1] == "AND":
        token = self.current
        self.n()
        res = Tree(res, token, self._factor())
      return res

    def _factor(self):
      token = self.current
      if token[1] == "LBR":
        self.n()
        res = self._or()
        if self.current[1] != "RBR":
          raise Exception(f"Not closed bracket! {res} {self.current}")
        self.n()
        return res
      elif token[1] == "CHR":
        self.n()
        return Tree(None, token, None)
      elif token[1] == "NOT":
        self.n()
        return Tree(None, token, self._factor())
      elif token[1] == "END":
        raise Exception("Unexpected end of input")
      else:
        raise Exception(f"Illegal token: {token}")

  return Parser(tokens).parse()

if __name__ == "__main__":
    logik = """
    (p ∧ ((q ∧ (r ∨ (¬r ∧ x ∧ ¬z))) ∨ (¬q ∧ ((r ∧ x ∧ z) ∨ (¬r ∧ (x ∨ (¬x ∧ ¬y ∧ ¬z)))))))∨
    (¬p ∧ ((q ∧ ((r ∧ x) ∨ (¬r ∧ z))) ∨ (¬q ∧ ((r ∧ (x ∨ (¬x ∧ (y ∨ (¬y ∧ z))))) ∨ (¬r ∧ x ∧ z)))))
    """

    #          x y: (x: var indecies, ...) | (y: var indecies, ...)
    vorlage = "8 8: p 2 3 6 7, y 5 6 7 8, r 3 4 5 6 | q 2 3 6 7, z 5 6 7 8, x 3 4 5 6"

    vl = parse_vorlage(vorlage)
    log = parse_logik(logik)

    img = log.execute(vl).draw(vl)
    img.show()
