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
        self.skipTest('not implement')

    def test_cut(self):
        self.skipTest('not implement')

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
        self.assertAlmostEqual(len(DayuTimeRange(DayuTimeCode(0), DayuTimeCode(0))), 0)
        self.assertAlmostEqual(len(DayuTimeRange(DayuTimeCode(0), DayuTimeCode(-1))), 1)

    def test___nonzero__(self):
        self.assertTrue(DayuTimeRange(DayuTimeCode(0), DayuTimeCode(140)))
        self.assertTrue(DayuTimeRange(DayuTimeCode(-100), DayuTimeCode(140)))
        self.assertFalse(DayuTimeRange(DayuTimeCode(-100), DayuTimeCode(-100)))
        self.assertFalse(DayuTimeRange(DayuTimeCode(0), DayuTimeCode(0)))

    def test___contains__(self):
        tr = DayuTimeRange(DayuTimeCode(0), DayuTimeCode(2880))
        for tc in DayuTimeRange(DayuTimeCode(-100), DayuTimeCode(14400)):
            if tr.start <= tc <= tr.end:
                self.assertTrue(tc in tr)
            else:
                self.assertFalse(tc in tr)
