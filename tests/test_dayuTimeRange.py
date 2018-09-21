#!/usr/bin/env python
# -*- encoding: utf-8 -*-

__author__ = 'andyguo'

from unittest import TestCase
from dayu_timecode.base import DayuTimeRange, DayuTimeCode
from dayu_timecode.error import *


class TestDayuTimeRange(TestCase):
    def test___new__(self):
        a = DayuTimeCode(100)
        b = DayuTimeCode(140)
        c = DayuTimeCode(140, fps=25)
        self.assertRaises(DayuTimeRangeValueError, DayuTimeRange, 1, 2)
        self.assertRaises(DayuTimeRangeValueError, DayuTimeRange, '00:00:00:00', 2)
        self.assertRaises(DayuTimeRangeValueError, DayuTimeRange, '00:00:00:00', '00:00:01:22')
        self.assertRaises(DayuTimeRangeFpsNotIdenticalError, DayuTimeRange, a, c)
        self.assertRaises(DayuTimeRangeOutOfRange, DayuTimeRange, DayuTimeCode(10), DayuTimeCode(10))
        tr = DayuTimeRange(a, b)
        self.assertEqual(tr.start, a)
        self.assertEqual(tr.end, b)
        self.assertIsNot(tr.start, a)
        self.assertIsNot(tr.end, b)
        tr = DayuTimeRange(b, a)
        self.assertEqual(tr.start, a)
        self.assertEqual(tr.end, b)

        d = a
        self.assertIs(a, d)
        d = DayuTimeCode(a.time, a.fps)
        self.assertIsNot(a, d)
        self.assertIsNot(a.time, d.time)

    def test_duration(self):
        self.assertEqual(DayuTimeRange(DayuTimeCode(0), DayuTimeCode(100)).duration, 100)
        self.assertEqual(DayuTimeRange(DayuTimeCode(-100), DayuTimeCode(-50)).duration, 50)
        self.assertEqual(DayuTimeRange(DayuTimeCode(-100), DayuTimeCode(50)).duration, 150)

    def test_cut(self):
        tr = DayuTimeRange(DayuTimeCode(0), DayuTimeCode(100))
        result = tr.cut(DayuTimeCode(50))
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].start, 0)
        self.assertEqual(result[0].end, 50)
        self.assertEqual(result[1].start, 50)
        self.assertEqual(result[1].end, 100)
        result = tr.cut(DayuTimeCode(-100))
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].start, 0)
        self.assertEqual(result[0].end, 100)
        result = tr.cut(DayuTimeCode(0))
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].start, 0)
        self.assertEqual(result[0].end, 100)
        result = tr.cut(DayuTimeCode(0))
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].start, 0)
        self.assertEqual(result[0].end, 100)
        result = tr.cut(DayuTimeCode(200))
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].start, 0)
        self.assertEqual(result[0].end, 100)

    def test_handle(self):
        tr = DayuTimeRange(DayuTimeCode(0), DayuTimeCode(140))
        tr.handle(10)
        self.assertAlmostEqual(tr.start, -10)
        self.assertAlmostEqual(tr.end, 150)
        tr.handle(-20)
        self.assertAlmostEqual(tr.start, 10)
        self.assertAlmostEqual(tr.end, 130)
        tr.handle(8, 3)
        self.assertAlmostEqual(tr.start, 2)
        self.assertAlmostEqual(tr.end, 133)
        self.assertRaises(DayuTimeRangeOutOfRange, tr.handle, -300)

    def test___iter__(self):
        a = DayuTimeCode(-2880)
        b = DayuTimeCode('1200s')
        current = DayuTimeCode(a.time, a.fps)
        x = None
        tr = DayuTimeRange(a, b)
        for x in tr:
            self.assertAlmostEqual(x, current)
            current += 1
        else:
            self.assertAlmostEqual(x, b - 1)
        self.assertEqual(tr.start, a)
        self.assertEqual(tr.end, b)

    def test___len__(self):
        self.assertAlmostEqual(len(DayuTimeRange(DayuTimeCode(0), DayuTimeCode(140))), 140)
        self.assertAlmostEqual(len(DayuTimeRange(DayuTimeCode(-100), DayuTimeCode(140))), 240)
        self.assertAlmostEqual(len(DayuTimeRange(DayuTimeCode(0), DayuTimeCode(-1))), 1)

    def test___nonzero__(self):
        self.assertTrue(DayuTimeRange(DayuTimeCode(0), DayuTimeCode(140)))
        self.assertTrue(DayuTimeRange(DayuTimeCode(-100), DayuTimeCode(140)))

    def test___contains__(self):
        tr = DayuTimeRange(DayuTimeCode(0), DayuTimeCode(2880))
        for tc in DayuTimeRange(DayuTimeCode(-100), DayuTimeCode(14400)):
            if tr.start <= tc <= tr.end:
                self.assertTrue(tc in tr)
            else:
                self.assertFalse(tc in tr)

        self.assertFalse(DayuTimeRange(DayuTimeCode(-200), DayuTimeCode(-150)) in tr)
        self.assertFalse(DayuTimeRange(DayuTimeCode(-200), DayuTimeCode(-100)) in tr)
        self.assertFalse(DayuTimeRange(DayuTimeCode(-200), DayuTimeCode(50)) in tr)
        self.assertFalse(DayuTimeRange(DayuTimeCode(-200), DayuTimeCode(2880)) in tr)
        self.assertFalse(DayuTimeRange(DayuTimeCode(-200), DayuTimeCode(30000)) in tr)
        self.assertTrue(DayuTimeRange(DayuTimeCode(0), DayuTimeCode(50)) in tr)
        self.assertTrue(DayuTimeRange(DayuTimeCode(0), DayuTimeCode(2880)) in tr)
        self.assertFalse(DayuTimeRange(DayuTimeCode(0), DayuTimeCode(30000)) in tr)
        self.assertTrue(DayuTimeRange(DayuTimeCode(50), DayuTimeCode(100)) in tr)
        self.assertTrue(DayuTimeRange(DayuTimeCode(50), DayuTimeCode(2880)) in tr)
        self.assertFalse(DayuTimeRange(DayuTimeCode(50), DayuTimeCode(3000)) in tr)
        self.assertFalse(DayuTimeRange(DayuTimeCode(2880), DayuTimeCode(2881)) in tr)
        self.assertFalse(DayuTimeRange(DayuTimeCode(2880), DayuTimeCode(30000)) in tr)

    def test___and__(self):
        a = DayuTimeRange(DayuTimeCode(0), DayuTimeCode(100))
        b = DayuTimeRange(DayuTimeCode(-200), DayuTimeCode(-100))
        c = DayuTimeRange(DayuTimeCode(-200), DayuTimeCode(20))
        d = DayuTimeRange(DayuTimeCode(-200), DayuTimeCode(100))
        e = DayuTimeRange(DayuTimeCode(-200), DayuTimeCode(400))
        self.assertIsNone(a & b)
        self.assertEqual(a & c, DayuTimeRange(DayuTimeCode(0), DayuTimeCode(20)))
        self.assertEqual(a & d, DayuTimeRange(DayuTimeCode(0), DayuTimeCode(100)))
        self.assertEqual(a & e, DayuTimeRange(DayuTimeCode(0), DayuTimeCode(100)))
        b = DayuTimeRange(DayuTimeCode(-1), DayuTimeCode(0))
        c = DayuTimeRange(DayuTimeCode(0), DayuTimeCode(20))
        d = DayuTimeRange(DayuTimeCode(0), DayuTimeCode(100))
        e = DayuTimeRange(DayuTimeCode(0), DayuTimeCode(400))
        self.assertIsNone(a & b)
        self.assertEqual(a & c, DayuTimeRange(DayuTimeCode(0), DayuTimeCode(20)))
        self.assertEqual(a & d, DayuTimeRange(DayuTimeCode(0), DayuTimeCode(100)))
        self.assertEqual(a & e, DayuTimeRange(DayuTimeCode(0), DayuTimeCode(100)))
        b = DayuTimeRange(DayuTimeCode(19), DayuTimeCode(20))
        c = DayuTimeRange(DayuTimeCode(20), DayuTimeCode(50))
        d = DayuTimeRange(DayuTimeCode(20), DayuTimeCode(100))
        e = DayuTimeRange(DayuTimeCode(20), DayuTimeCode(400))
        self.assertEqual(a & b, DayuTimeRange(DayuTimeCode(19), DayuTimeCode(20)))
        self.assertEqual(a & c, DayuTimeRange(DayuTimeCode(20), DayuTimeCode(50)))
        self.assertEqual(a & d, DayuTimeRange(DayuTimeCode(20), DayuTimeCode(100)))
        self.assertEqual(a & e, DayuTimeRange(DayuTimeCode(20), DayuTimeCode(100)))
        b = DayuTimeRange(DayuTimeCode(100), DayuTimeCode(101))
        c = DayuTimeRange(DayuTimeCode(100), DayuTimeCode(400))
        self.assertIsNone(a & b)
        self.assertIsNone(a & c)
        b = DayuTimeRange(DayuTimeCode(200), DayuTimeCode(400))
        c = DayuTimeRange(DayuTimeCode(400), DayuTimeCode(401))
        self.assertIsNone(a & b)
        self.assertIsNone(a & c)

    def test___or__(self):
        a = DayuTimeRange(DayuTimeCode(0), DayuTimeCode(100))
        b = DayuTimeRange(DayuTimeCode(-200), DayuTimeCode(-100))
        c = DayuTimeRange(DayuTimeCode(-200), DayuTimeCode(20))
        d = DayuTimeRange(DayuTimeCode(-200), DayuTimeCode(100))
        e = DayuTimeRange(DayuTimeCode(-200), DayuTimeCode(400))
        self.assertEqual(a | b, DayuTimeRange(DayuTimeCode(-200), DayuTimeCode(100)))
        self.assertEqual(a | c, DayuTimeRange(DayuTimeCode(-200), DayuTimeCode(100)))
        self.assertEqual(a | d, DayuTimeRange(DayuTimeCode(-200), DayuTimeCode(100)))
        self.assertEqual(a | e, DayuTimeRange(DayuTimeCode(-200), DayuTimeCode(400)))
        b = DayuTimeRange(DayuTimeCode(-1), DayuTimeCode(0))
        c = DayuTimeRange(DayuTimeCode(0), DayuTimeCode(20))
        d = DayuTimeRange(DayuTimeCode(0), DayuTimeCode(100))
        e = DayuTimeRange(DayuTimeCode(0), DayuTimeCode(400))
        self.assertEqual(a | b, DayuTimeRange(DayuTimeCode(-1), DayuTimeCode(100)))
        self.assertEqual(a | c, DayuTimeRange(DayuTimeCode(0), DayuTimeCode(100)))
        self.assertEqual(a | d, DayuTimeRange(DayuTimeCode(0), DayuTimeCode(100)))
        self.assertEqual(a | e, DayuTimeRange(DayuTimeCode(0), DayuTimeCode(400)))
        b = DayuTimeRange(DayuTimeCode(19), DayuTimeCode(20))
        c = DayuTimeRange(DayuTimeCode(20), DayuTimeCode(50))
        d = DayuTimeRange(DayuTimeCode(20), DayuTimeCode(100))
        e = DayuTimeRange(DayuTimeCode(20), DayuTimeCode(400))
        self.assertEqual(a | b, DayuTimeRange(DayuTimeCode(0), DayuTimeCode(100)))
        self.assertEqual(a | c, DayuTimeRange(DayuTimeCode(0), DayuTimeCode(100)))
        self.assertEqual(a | d, DayuTimeRange(DayuTimeCode(0), DayuTimeCode(100)))
        self.assertEqual(a | e, DayuTimeRange(DayuTimeCode(0), DayuTimeCode(400)))
        b = DayuTimeRange(DayuTimeCode(100), DayuTimeCode(101))
        c = DayuTimeRange(DayuTimeCode(100), DayuTimeCode(400))
        self.assertEqual(a | b, DayuTimeRange(DayuTimeCode(0), DayuTimeCode(101)))
        self.assertEqual(a | c, DayuTimeRange(DayuTimeCode(0), DayuTimeCode(400)))
        b = DayuTimeRange(DayuTimeCode(200), DayuTimeCode(400))
        c = DayuTimeRange(DayuTimeCode(400), DayuTimeCode(401))
        self.assertEqual(a | b, DayuTimeRange(DayuTimeCode(0), DayuTimeCode(400)))
        self.assertEqual(a | c, DayuTimeRange(DayuTimeCode(0), DayuTimeCode(401)))

    def test___xor__(self):
        a = DayuTimeRange(DayuTimeCode(0), DayuTimeCode(100))
        b = DayuTimeRange(DayuTimeCode(-200), DayuTimeCode(-100))
        c = DayuTimeRange(DayuTimeCode(-200), DayuTimeCode(20))
        d = DayuTimeRange(DayuTimeCode(-200), DayuTimeCode(100))
        e = DayuTimeRange(DayuTimeCode(-200), DayuTimeCode(400))
        self.assertEqual(a ^ b,
                         (DayuTimeRange(DayuTimeCode(-200), DayuTimeCode(-100)),
                          DayuTimeRange(DayuTimeCode(0), DayuTimeCode(100))))
        self.assertEqual(a ^ c,
                         (DayuTimeRange(DayuTimeCode(-200), DayuTimeCode(0)),
                          DayuTimeRange(DayuTimeCode(20), DayuTimeCode(100))))
        self.assertEqual(a ^ d,
                         (DayuTimeRange(DayuTimeCode(-200), DayuTimeCode(0)),
                          None))
        self.assertEqual(a ^ e,
                         (DayuTimeRange(DayuTimeCode(-200), DayuTimeCode(0)),
                          DayuTimeRange(DayuTimeCode(100), DayuTimeCode(400))))

        b = DayuTimeRange(DayuTimeCode(-1), DayuTimeCode(0))
        c = DayuTimeRange(DayuTimeCode(0), DayuTimeCode(20))
        d = DayuTimeRange(DayuTimeCode(0), DayuTimeCode(100))
        e = DayuTimeRange(DayuTimeCode(0), DayuTimeCode(400))
        self.assertEqual(a ^ b,
                         (DayuTimeRange(DayuTimeCode(-1), DayuTimeCode(-0)),
                          DayuTimeRange(DayuTimeCode(0), DayuTimeCode(100))))
        self.assertEqual(a ^ c,
                         (None,
                          DayuTimeRange(DayuTimeCode(20), DayuTimeCode(100))))
        self.assertEqual(a ^ d,
                         (None,
                          None))
        self.assertEqual(a ^ e,
                         (None,
                          DayuTimeRange(DayuTimeCode(100), DayuTimeCode(400))))

        b = DayuTimeRange(DayuTimeCode(19), DayuTimeCode(20))
        c = DayuTimeRange(DayuTimeCode(20), DayuTimeCode(50))
        d = DayuTimeRange(DayuTimeCode(20), DayuTimeCode(100))
        e = DayuTimeRange(DayuTimeCode(20), DayuTimeCode(400))
        self.assertEqual(a ^ b,
                         (DayuTimeRange(DayuTimeCode(-0), DayuTimeCode(19)),
                          DayuTimeRange(DayuTimeCode(20), DayuTimeCode(100))))
        self.assertEqual(a ^ c,
                         (DayuTimeRange(DayuTimeCode(0), DayuTimeCode(20)),
                          DayuTimeRange(DayuTimeCode(50), DayuTimeCode(100))))
        self.assertEqual(a ^ d,
                         (DayuTimeRange(DayuTimeCode(0), DayuTimeCode(20)),
                          None))
        self.assertEqual(a ^ e,
                         (DayuTimeRange(DayuTimeCode(0), DayuTimeCode(20)),
                          DayuTimeRange(DayuTimeCode(100), DayuTimeCode(400))))

        b = DayuTimeRange(DayuTimeCode(100), DayuTimeCode(101))
        c = DayuTimeRange(DayuTimeCode(100), DayuTimeCode(400))
        self.assertEqual(a ^ b,
                         (DayuTimeRange(DayuTimeCode(0), DayuTimeCode(100)),
                          DayuTimeRange(DayuTimeCode(100), DayuTimeCode(101))))
        self.assertEqual(a ^ c,
                         (DayuTimeRange(DayuTimeCode(0), DayuTimeCode(100)),
                          DayuTimeRange(DayuTimeCode(100), DayuTimeCode(400))))
        b = DayuTimeRange(DayuTimeCode(200), DayuTimeCode(400))
        c = DayuTimeRange(DayuTimeCode(400), DayuTimeCode(401))
        self.assertEqual(a ^ b,
                         (DayuTimeRange(DayuTimeCode(0), DayuTimeCode(100)),
                          DayuTimeRange(DayuTimeCode(200), DayuTimeCode(400))))
        self.assertEqual(a ^ c,
                         (DayuTimeRange(DayuTimeCode(0), DayuTimeCode(100)),
                          DayuTimeRange(DayuTimeCode(400), DayuTimeCode(401))))

    def test___iadd__(self):
        a = DayuTimeRange(DayuTimeCode(0), DayuTimeCode(100))
        a += DayuTimeCode(100)
        self.assertEqual(a, DayuTimeRange(DayuTimeCode(100), DayuTimeCode(200)))
        a += 1
        self.assertEqual(a, DayuTimeRange(DayuTimeCode(101), DayuTimeCode(201)))
        a += 10.0
        self.assertAlmostEqual(a, DayuTimeRange(DayuTimeCode(111), DayuTimeCode(211)))
        a += (-20)
        self.assertAlmostEqual(a, DayuTimeRange(DayuTimeCode(91), DayuTimeCode(191)))
        self.assertRaises((DayuTimeRangeOutOfRange, DayuTimeRangeOperationError, TypeError, ValueError),
                          lambda: a + None)
        self.assertRaises((DayuTimeRangeOutOfRange, DayuTimeRangeOperationError, TypeError, ValueError), lambda: a + '')
        self.assertRaises((DayuTimeRangeOutOfRange, DayuTimeRangeOperationError, TypeError, ValueError), lambda: a + a)
        self.assertRaises((DayuTimeRangeOutOfRange, DayuTimeRangeOperationError, TypeError, ValueError), lambda: a + [])
        self.assertRaises((DayuTimeRangeOutOfRange, DayuTimeRangeOperationError, TypeError, ValueError),
                          lambda: a + tuple)

    def test___add__(self):
        a = DayuTimeRange(DayuTimeCode(0), DayuTimeCode(100))
        self.assertEqual(a + DayuTimeCode(100), DayuTimeRange(DayuTimeCode(100), DayuTimeCode(200)))
        self.assertEqual(a + 0, DayuTimeRange(DayuTimeCode(0), DayuTimeCode(100)))
        self.assertEqual(a + 100, DayuTimeRange(DayuTimeCode(100), DayuTimeCode(200)))
        self.assertEqual(a + (-100), DayuTimeRange(DayuTimeCode(-100), DayuTimeCode(0)))
        self.assertRaises(DayuTimeRangeOperationError, lambda: a + None)
        self.assertRaises(DayuTimeRangeOperationError, lambda: a + '')
        self.assertRaises(DayuTimeRangeOperationError, lambda: a + a)
        self.assertRaises(DayuTimeRangeOperationError, lambda: a + [])
        self.assertRaises(DayuTimeRangeOperationError, lambda: a + tuple)

    def test___sub__(self):
        a = DayuTimeRange(DayuTimeCode(0), DayuTimeCode(100))
        self.assertEqual(a - DayuTimeCode(100), DayuTimeRange(DayuTimeCode(-100), DayuTimeCode(0)))
        self.assertEqual(a - 0, DayuTimeRange(DayuTimeCode(0), DayuTimeCode(100)))
        self.assertEqual(a - 100, DayuTimeRange(DayuTimeCode(-100), DayuTimeCode(0)))
        self.assertEqual(a - (-100), DayuTimeRange(DayuTimeCode(100), DayuTimeCode(200)))
        self.assertRaises((DayuTimeRangeOutOfRange, DayuTimeRangeOperationError, TypeError, ValueError),
                          lambda: a - None)
        self.assertRaises((DayuTimeRangeOutOfRange, DayuTimeRangeOperationError, TypeError, ValueError), lambda: a - '')
        self.assertRaises((DayuTimeRangeOutOfRange, DayuTimeRangeOperationError, TypeError, ValueError), lambda: a - a)
        self.assertRaises((DayuTimeRangeOutOfRange, DayuTimeRangeOperationError, TypeError, ValueError), lambda: a - [])
        self.assertRaises((DayuTimeRangeOutOfRange, DayuTimeRangeOperationError, TypeError, ValueError),
                          lambda: a - tuple)

    def test___isub__(self):
        a = DayuTimeRange(DayuTimeCode(0), DayuTimeCode(100))
        a -= DayuTimeCode(100)
        self.assertEqual(a, DayuTimeRange(DayuTimeCode(-100), DayuTimeCode(0)))
        a -= 1
        self.assertEqual(a, DayuTimeRange(DayuTimeCode(-101), DayuTimeCode(-1)))
        a -= 10.0
        self.assertAlmostEqual(a, DayuTimeRange(DayuTimeCode(-111), DayuTimeCode(-11)))
        a -= (-20)
        self.assertAlmostEqual(a, DayuTimeRange(DayuTimeCode(-91), DayuTimeCode(9)))
        self.assertRaises((DayuTimeRangeOutOfRange, DayuTimeRangeOperationError, TypeError, ValueError),
                          lambda: a - None)
        self.assertRaises((DayuTimeRangeOutOfRange, DayuTimeRangeOperationError, TypeError, ValueError), lambda: a - '')
        self.assertRaises((DayuTimeRangeOutOfRange, DayuTimeRangeOperationError, TypeError, ValueError), lambda: a - a)
        self.assertRaises((DayuTimeRangeOutOfRange, DayuTimeRangeOperationError, TypeError, ValueError), lambda: a + [])
        self.assertRaises((DayuTimeRangeOutOfRange, DayuTimeRangeOperationError, TypeError, ValueError),
                          lambda: a + tuple)

    def test___mul__(self):
        a = DayuTimeRange(DayuTimeCode(0), DayuTimeCode(100))
        self.assertEqual(a * DayuTimeCode(3), DayuTimeRange(DayuTimeCode(0), DayuTimeCode(300)))
        self.assertEqual(a * 0.5, DayuTimeRange(DayuTimeCode(0), DayuTimeCode(50)))
        self.assertRaises((DayuTimeRangeOutOfRange, DayuTimeRangeOperationError), lambda: a * 0)
        self.assertEqual(a * 3, DayuTimeRange(DayuTimeCode(0), DayuTimeCode(300)))
        self.assertEqual(a * 3.5, DayuTimeRange(DayuTimeCode(0), DayuTimeCode(350)))
        self.assertEqual(a * -1, DayuTimeRange(DayuTimeCode(-100), DayuTimeCode(0)))
        a = DayuTimeRange(DayuTimeCode(100), DayuTimeCode(200))
        self.assertEqual(a * DayuTimeCode(3), DayuTimeRange(DayuTimeCode(100), DayuTimeCode(400)))
        self.assertEqual(a * 3, DayuTimeRange(DayuTimeCode(100), DayuTimeCode(400)))
        self.assertEqual(a * 3.5, DayuTimeRange(DayuTimeCode(100), DayuTimeCode(450)))
        self.assertEqual(a * -1, DayuTimeRange(DayuTimeCode(0), DayuTimeCode(100)))
        self.assertEqual(a * -1.5, DayuTimeRange(DayuTimeCode(-50), DayuTimeCode(100)))
        self.assertRaises((DayuTimeRangeOutOfRange, DayuTimeRangeOperationError, TypeError, ValueError),
                          lambda: a * None)
        self.assertRaises((DayuTimeRangeOutOfRange, DayuTimeRangeOperationError, TypeError, ValueError), lambda: a * '')
        self.assertRaises((DayuTimeRangeOutOfRange, DayuTimeRangeOperationError, TypeError, ValueError), lambda: a * a)
        self.assertRaises((DayuTimeRangeOutOfRange, DayuTimeRangeOperationError, TypeError, ValueError), lambda: a * [])
        self.assertRaises((DayuTimeRangeOutOfRange, DayuTimeRangeOperationError, TypeError, ValueError),
                          lambda: a * tuple)

    def test___imul__(self):
        a = DayuTimeRange(DayuTimeCode(0), DayuTimeCode(100))
        a *= DayuTimeCode(3)
        self.assertEqual(a, DayuTimeRange(DayuTimeCode(0), DayuTimeCode(300)))
        a *= 0.5
        self.assertEqual(a, DayuTimeRange(DayuTimeCode(0), DayuTimeCode(150)))
        self.assertEqual(a * -1, DayuTimeRange(DayuTimeCode(-150), DayuTimeCode(0)))
        a = DayuTimeRange(DayuTimeCode(100), DayuTimeCode(200))
        a *= 3
        self.assertEqual(a, DayuTimeRange(DayuTimeCode(100), DayuTimeCode(400)))
        a *= 0.5
        self.assertEqual(a, DayuTimeRange(DayuTimeCode(100), DayuTimeCode(250)))
        a *= (-1)
        print a.start, a.end
        self.assertEqual(a, DayuTimeRange(DayuTimeCode(-50), DayuTimeCode(100)))

    def test___div__(self):
        a = DayuTimeRange(DayuTimeCode(0), DayuTimeCode(100))
        self.assertEqual(a / DayuTimeCode(2), DayuTimeRange(DayuTimeCode(0), DayuTimeCode(50)))
        self.assertRaises(ZeroDivisionError, lambda: a / 0)
        self.assertEqual(a / 0.2, DayuTimeRange(DayuTimeCode(0), DayuTimeCode(500)))
        self.assertEqual(a / 20, DayuTimeRange(DayuTimeCode(0), DayuTimeCode(5)))
        self.assertEqual(a / -1, DayuTimeRange(DayuTimeCode(-100), DayuTimeCode(0)))
        a = DayuTimeRange(DayuTimeCode(100), DayuTimeCode(200))
        self.assertEqual(a / DayuTimeCode(2), DayuTimeRange(DayuTimeCode(100), DayuTimeCode(150)))
        self.assertEqual(a / 0.5, DayuTimeRange(DayuTimeCode(100), DayuTimeCode(300)))
        self.assertEqual(a / 20, DayuTimeRange(DayuTimeCode(100), DayuTimeCode(105)))
        self.assertEqual(a / -1, DayuTimeRange(DayuTimeCode(0), DayuTimeCode(100)))
        self.assertEqual(a / -2, DayuTimeRange(DayuTimeCode(50), DayuTimeCode(100)))
        self.assertRaises((DayuTimeRangeOutOfRange, DayuTimeRangeOperationError, TypeError, ValueError),
                          lambda: a / None)
        self.assertRaises((DayuTimeRangeOutOfRange, DayuTimeRangeOperationError, TypeError, ValueError), lambda: a / '')
        self.assertRaises((DayuTimeRangeOutOfRange, DayuTimeRangeOperationError, TypeError, ValueError), lambda: a / a)
        self.assertRaises((DayuTimeRangeOutOfRange, DayuTimeRangeOperationError, TypeError, ValueError), lambda: a / [])
        self.assertRaises((DayuTimeRangeOutOfRange, DayuTimeRangeOperationError, TypeError, ValueError),
                          lambda: a / tuple)

    def test___idiv__(self):
        a = DayuTimeRange(DayuTimeCode(0), DayuTimeCode(100))
        a /= 2
        self.assertEqual(a, DayuTimeRange(DayuTimeCode(0), DayuTimeCode(50)))
        self.assertRaises(ZeroDivisionError, lambda: a / 0)
        a /= 0.2
        self.assertEqual(a, DayuTimeRange(DayuTimeCode(0), DayuTimeCode(250)))
        a /= 10
        self.assertEqual(a, DayuTimeRange(DayuTimeCode(0), DayuTimeCode(25)))
        a /= -1
        self.assertEqual(a, DayuTimeRange(DayuTimeCode(-25), DayuTimeCode(0)))
        a = DayuTimeRange(DayuTimeCode(100), DayuTimeCode(200))
        a /= 2
        self.assertEqual(a, DayuTimeRange(DayuTimeCode(100), DayuTimeCode(150)))
        a /= 0.5
        self.assertEqual(a, DayuTimeRange(DayuTimeCode(100), DayuTimeCode(200)))
        a /= 20
        self.assertEqual(a, DayuTimeRange(DayuTimeCode(100), DayuTimeCode(105)))
        a /= -0.5
        self.assertEqual(a, DayuTimeRange(DayuTimeCode(90), DayuTimeCode(100)))
        a /= -0.01
        self.assertEqual(a, DayuTimeRange(DayuTimeCode(-910), DayuTimeCode(90)))

    def test___lshift__(self):
        a = DayuTimeRange(DayuTimeCode(0), DayuTimeCode(100))
        self.assertEqual(a << 0, DayuTimeRange(DayuTimeCode(0), DayuTimeCode(100)))
        self.assertEqual(a << 10, DayuTimeRange(DayuTimeCode(-10), DayuTimeCode(100)))
        self.assertEqual(a << 100, DayuTimeRange(DayuTimeCode(-100), DayuTimeCode(100)))
        self.assertEqual(a << -10, DayuTimeRange(DayuTimeCode(10), DayuTimeCode(100)))
        self.assertRaises((DayuTimeRangeOperationError, DayuTimeRangeOutOfRange), lambda: a << -100)
        self.assertRaises((DayuTimeRangeOperationError, DayuTimeRangeOutOfRange), lambda: a << -200)
        self.assertRaises((DayuTimeRangeOperationError, DayuTimeRangeOutOfRange), lambda: a << None)
        self.assertRaises((DayuTimeRangeOperationError, DayuTimeRangeOutOfRange), lambda: a << '')
        self.assertRaises((DayuTimeRangeOperationError, DayuTimeRangeOutOfRange), lambda: a << [])
        self.assertRaises((DayuTimeRangeOperationError, DayuTimeRangeOutOfRange), lambda: a << tuple())

    def test___Rshift__(self):
        a = DayuTimeRange(DayuTimeCode(0), DayuTimeCode(100))
        self.assertEqual(a >> 0, DayuTimeRange(DayuTimeCode(0), DayuTimeCode(100)))
        self.assertEqual(a >> 10, DayuTimeRange(DayuTimeCode(0), DayuTimeCode(110)))
        self.assertEqual(a >> 100, DayuTimeRange(DayuTimeCode(0), DayuTimeCode(200)))
        self.assertEqual(a >> -10, DayuTimeRange(DayuTimeCode(0), DayuTimeCode(90)))
        self.assertRaises((DayuTimeRangeOperationError, DayuTimeRangeOutOfRange), lambda: a >> -100)
        self.assertRaises((DayuTimeRangeOperationError, DayuTimeRangeOutOfRange), lambda: a >> -200)
        self.assertRaises((DayuTimeRangeOperationError, DayuTimeRangeOutOfRange), lambda: a >> None)
        self.assertRaises((DayuTimeRangeOperationError, DayuTimeRangeOutOfRange), lambda: a >> '')
        self.assertRaises((DayuTimeRangeOperationError, DayuTimeRangeOutOfRange), lambda: a >> [])
        self.assertRaises((DayuTimeRangeOperationError, DayuTimeRangeOutOfRange), lambda: a >> tuple())

    def test___eq__(self):
        self.assertTrue(DayuTimeRange(DayuTimeCode(0), DayuTimeCode(100)),
                        DayuTimeRange(DayuTimeCode(0), DayuTimeCode(100)))
        self.assertTrue(DayuTimeRange(DayuTimeCode(0), DayuTimeCode(100)),
                        DayuTimeRange(DayuTimeCode(0), DayuTimeCode(100)) * 3 / 3.0)
        self.assertTrue(DayuTimeRange(DayuTimeCode(0), DayuTimeCode(100)),
                        DayuTimeRange(DayuTimeCode(0), DayuTimeCode(100.0000001)))
        self.assertTrue(DayuTimeRange(DayuTimeCode(0), DayuTimeCode(100)),
                        DayuTimeRange(DayuTimeCode(0.0000001), DayuTimeCode(100)))
        self.assertTrue(DayuTimeRange(DayuTimeCode(0), DayuTimeCode(100)),
                        DayuTimeRange(DayuTimeCode(-0.0000001), DayuTimeCode(100)))
        self.assertTrue(DayuTimeRange(DayuTimeCode(0), DayuTimeCode(100)),
                        DayuTimeRange(DayuTimeCode(0), DayuTimeCode(99.9999999)))
