class QueueUnderflow(ValueError):
    pass

class SQueue(object):
    def __init__(self, init_len=8):
        self._len = init_len
        self._elems = [0] * init_len
        self._head = 0
        self._num = 0

    def is_empty(self):
        return self._num == 0

    def peek(self):
        if self.is_empty():
            raise QueueUnderflow
        else:
            return self._elems[self._head]

    def dequeue(self):
        if self.is_empty():
            raise QueueUnderflow
        else:
            e = self._elems[self._head]
            self._head = (self._head + 1) % self._len
            self._num -= 1
            return e

    def enqueue(self, new_ele):
        if self._num == self._len:
            self.__extend()
        self._elems[(self._head + self._num) % self._len] = new_ele
        self._num += 1

    def __extend(self):
        old_len = self._len
        self._len *= 2
        new_elems = [0] * self._len
        for i in range(old_len):
            new_elems[i] = self._elems[(self._head + i) % old_len]
        self._elems, self._head = new_elems, 0

S = SQueue(13)
S.enqueue(12)
S.enqueue(3)
print(S)
print(S.dequeue())
print(S.dequeue())
print(S.dequeue())