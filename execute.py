import sys

with open(sys.argv[1], "r") as f:
  code = f.read().replace("\n", "")

def call(s, a, c = 0):
  b = functions[a[0]][1](s, *a[1])
  return v(b) if c else b

def v(c):
  while isinstance(c, list):
    c = com(0, c)[-1]
  return c

def com(a, b):
  return (
    (a if isinstance(a, list) else [a]) +
    (b if isinstance(b, list) else [b])
  )

def throw(e):
  raise e

functions = {
  "L": [0, lambda s: s.last],
  "A": [0, lambda s: s.args],
  ":": [3, lambda s, a, b, c:
    [
      functions.update([[
        a[0],
        [
          d := call(s, b, 1),
          lambda s, *e: [
            setattr(s, "args", [*map(lambda d: call(s, d), e)]),
            e := call(s, c)
          ][1],
        ]
      ]]),
      d
    ][1]
  ],
  "+": [2, lambda s, a, b: call(s, a, 1) + call(s, b, 1)],
  "-": [2, lambda s, a, b: call(s, a, 1) - call(s, b, 1)],
  "*": [2, lambda s, a, b: call(s, a, 1) * call(s, b, 1)],
  "/": [2, lambda s, a, b: [
    c := call(s, a, 1),
    d := call(s, b, 1) if c else c,
    c // d if d else d
  ][2]],
  "!": [1, lambda s, a: [
    b := call(s, a, 1),
    s.outputs[s.outputi].write(chr(b))
  ][0]],
  "?": [0, lambda s: [
    b := s.inputs[s.inputi].read(1),
    ord(b) if b else -1
  ][1]],
  ">": [2, lambda s, a, b: [
    c := call(s, a),
    c := com([], c),
    setattr(s, "last", []),
    setattr(s, "args", []),
    [[
      setattr(s, "args", com([], i)),
      setattr(s, "last", call(s, b))
    ] for i in c],
    s.last
  ][5]],
  "<": [3, lambda s, a, b, c: [
    [
      setattr(s, "last", call(s, c)) for i in
      iter(lambda: call(s, a), call(s, b))
    ],
    s.last
  ][1]],
  ",": [1, lambda s, a: [
    b := call(s, a),
    com(s.last, b)
  ][1]],
  "_": [2, lambda s, a, b: [
    c := com([], call(s, a)),
    d := call(s, b, 1),
    c[d] if d in range(-len(c), len(c)) else -1
  ][2]],
  "0": [0, lambda s: 0],
  "1": [0, lambda s: 1],
  "2": [0, lambda s: 2],
  "3": [0, lambda s: 3],
  "4": [0, lambda s: 4],
  "5": [0, lambda s: 5],
  "6": [0, lambda s: 6],
  "7": [0, lambda s: 7],
  "8": [0, lambda s: 8],
  "9": [0, lambda s: 9],
  "¡": [1, lambda s, a: [
    setattr(s, "outputi", b := call(s, a, 1) % len(s.outputs)),
    b
  ][1]],
  "¿": [1, lambda s, a: [
    setattr(s, "inputi", b := call(s, a, 1) % len(s.inputs)),
    b
  ][1]],
  "^": [0, lambda s: [
    b := "".join(map(chr, s.last)),
    c := open(b, "w"),
    s.outputs.append(c),
    len(s.outputs) - 1
  ][3]],
  "~": [0, lambda s: [
    b := "".join(map(chr, s.last)),
    c := open(b, "r"),
    s.inputs.append(c),
    len(s.inputs) - 1
  ][3]],
  "°": [0, lambda s: [
    s.outputs[s.outputi].close(),
    s.outputs.pop(s.outputi),
    len(s.outputs)
  ][2]],
  "=": [0, lambda s: [
    s.inputs[s.inputi].close(),
    s.inputs.pop(s.inputi),
    len(s.inputs)
  ][2]]
}

from sys import stdout, stdin, stderr, argv

class Code:
  def __init__(self, code):
    self.code = code
    self.i = 0
    self.last = []

    self.args = []
    for i in argv[1:]:
      self.args.append([*map(ord, i)])

    self.inputs = [stdin]
    self.outputs = [stdout, stderr]
    self.inputi = 0
    self.outputi = 0

  def run(self):
    while self.i < len(self.code):
      l = self.element()
      k = call(self, l)
      self.last = com([], k)

    for i in [*self.inputs, *self.outputs]:
      if i not in [stdin, stdout, stderr]:
        i.close()

  def element(self):
    ch = self.code[self.i]
    self.i += 1
    if ch in functions:
      f = functions[ch]
      argc = f[0]
      argv = []
      for i in range(argc):
        argv.append(self.element())
      return [ch, argv]
    else:
      return [ch, []]

c = Code(code)
c.run()
