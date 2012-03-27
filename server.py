import os
from itertools import combinations
from collections import defaultdict
import tornado.ioloop
import tornado.web
from freq_words import words


MAX_RESULTS = 500
MAX_CHARS = 12
MAX_LENGTH = 12
PORT = 4747


index = defaultdict(set)
for word in words.iterkeys():
  index[''.join(sorted(word.lower()))].add(word)


def search(chars, length):
  results = set()
  chars = ''.join(chars).lower()
  if len(chars) >= length:
    for comb in combinations(sorted(chars), length):
      results.update(index[''.join(comb)])
  return sorted(results, key=lambda x: -words[x])[:MAX_RESULTS]


class WordSearch(tornado.web.RequestHandler):

  def get(self):
    words, chars, length = [], [], None

    if 'char' in self.request.arguments:
      chars = self.request.arguments['char'][:MAX_CHARS]

    if 'length' in self.request.arguments:
      length = min(MAX_LENGTH, max(0, int(self.get_argument('length'))))

    if len(chars) > 0 and length != None:
      words = search(chars, length)

    self.render('./index.html', words=words, chars=chars, length=length)


if __name__ == '__main__':
  settings = {"static_path": os.path.join(os.path.dirname(__file__), "static")}
  application = tornado.web.Application([(r'/', WordSearch)], **settings)
  application.listen(PORT)
  tornado.ioloop.IOLoop.instance().start()
