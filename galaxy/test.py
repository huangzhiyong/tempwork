class A(object):
    def __init__(self):
        self.a = 'a'
        print 'A'

    def aa(self):
        print 'A:abc'


class B(object):
    def __init__(self):
        self.a = 'b'
        print 'B'

    def bb(self):
        print 'B:abc'


class C(object):
    def __init__(self):
        self.a = 'c'

    print 'C'

    def cc(self):
        print 'C:abc: %s' % (self.a)


class ABC(B,A,C):
    pass

a = ABC()
a.cc()