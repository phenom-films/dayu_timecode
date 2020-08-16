#!/usr/bin/env python
# -*- encoding: utf-8 -*-

__author__ = 'andyguo'

from unittest import TestCase
import copy
from dayu_timecode.base import DayuTimeCode, Fraction
from dayu_timecode.error import *
from dayu_timecode.config import *


class TestDayuTimeCode(TestCase):

    def test___new__(self):
        tc = DayuTimeCode(96)
        self.assertEqual((tc.time, tc.fps), (4, 24.0))
        tc = DayuTimeCode(100, 25)
        self.assertEqual((tc.time, tc.fps), (4, 25.0))
        self.assertIsInstance(tc.fps, float)
        self.assertIsInstance(tc.time, Fraction)

        tc = DayuTimeCode(11246.34)
        self.assertAlmostEqual(tc.time, 468.5975)
        self.assertEqual(tc.fps, 24.0)
        tc = DayuTimeCode(9876.142, 25.0)
        self.assertAlmostEqual(tc.time, 395.04568)
        self.assertIsInstance(tc.fps, float)
        self.assertIsInstance(tc.time, Fraction)

        tc = DayuTimeCode('0')
        self.assertAlmostEqual(tc.time, 0)
        tc = DayuTimeCode('00:00')
        self.assertAlmostEqual(tc.time, 0)
        tc = DayuTimeCode('00:00:00')
        self.assertAlmostEqual(tc.time, 0)
        tc = DayuTimeCode('00:00:00:00')
        self.assertAlmostEqual(tc.time, 0)
        tc = DayuTimeCode('1')
        self.assertAlmostEqual(tc.time, 0.04166666667)
        tc = DayuTimeCode('08')
        self.assertAlmostEqual(tc.time, 0.3333333333)
        tc = DayuTimeCode('1:8')
        self.assertAlmostEqual(tc.time, 1.3333333333)
        tc = DayuTimeCode('01:8')
        self.assertAlmostEqual(tc.time, 1.3333333333)
        tc = DayuTimeCode('01:08')
        self.assertAlmostEqual(tc.time, 1.3333333333)
        tc = DayuTimeCode('3:2:12')
        self.assertAlmostEqual(tc.time, 182.5)
        tc = DayuTimeCode('3:02:12')
        self.assertAlmostEqual(tc.time, 182.5)
        tc = DayuTimeCode('03:2:12')
        self.assertAlmostEqual(tc.time, 182.5)
        tc = DayuTimeCode('7:2:6:9')
        self.assertAlmostEqual(tc.time, 25326.375)
        tc = DayuTimeCode('7:2:6:09')
        self.assertAlmostEqual(tc.time, 25326.375)
        tc = DayuTimeCode('7:2:06:9')
        self.assertAlmostEqual(tc.time, 25326.375)
        tc = DayuTimeCode('7:02:6:9')
        self.assertAlmostEqual(tc.time, 25326.375)
        tc = DayuTimeCode('07:2:6:9')
        self.assertAlmostEqual(tc.time, 25326.375)
        tc = DayuTimeCode('7:2:06:09')
        self.assertAlmostEqual(tc.time, 25326.375)
        tc = DayuTimeCode('7:02:06:09')
        self.assertAlmostEqual(tc.time, 25326.375)
        tc = DayuTimeCode('07:02:06:09')
        self.assertAlmostEqual(tc.time, 25326.375)
        self.assertRaises(DayuTimeCodeValueError, DayuTimeCode, '7:2:6:60')
        self.assertRaises(DayuTimeCodeValueError, DayuTimeCode, '7:2:60:00')
        self.assertRaises(DayuTimeCodeValueError, DayuTimeCode, '7:60:60:00')
        self.assertRaises(DayuTimeCodeValueError, DayuTimeCode, '24:60:60:00')
        self.assertRaises(DayuTimeCodeValueError, DayuTimeCode, '24:60:60:60')
        self.assertRaises(DayuTimeCodeValueError, DayuTimeCode, '24:160:60:60')
        self.assertRaises(DayuTimeCodeValueError, DayuTimeCode, '24:60:260:60')
        self.assertRaises(DayuTimeCodeValueError, DayuTimeCode, '21:22:260:260')

        tc = DayuTimeCode('1;8', 29.97)
        self.assertAlmostEqual(tc.time, 1.2669336002669336)
        self.assertEqual(tc.fps, 29.97)
        tc = DayuTimeCode('1;08', 29.97)
        self.assertAlmostEqual(tc.time, 1.2669336002669336)
        tc = DayuTimeCode('01;08', 29.97)
        self.assertAlmostEqual(tc.time, 1.2669336002669336)
        tc = DayuTimeCode('00:00:00;00', 29.97)
        self.assertAlmostEqual(tc.time, 0.0)
        tc = DayuTimeCode('00:00:59;29', 29.97)
        self.assertAlmostEqual(tc.time, 59.96763430096763)
        tc = DayuTimeCode('00:01:00;02', 29.97)
        self.assertAlmostEqual(tc.time, 60.06673340006673)
        tc = DayuTimeCode('00:01:59;29', 29.97)
        self.assertAlmostEqual(tc.time, 119.96763430096763)
        tc = DayuTimeCode('00:02:00;02', 29.97)
        self.assertAlmostEqual(tc.time, 120.0667334001)
        tc = DayuTimeCode('00:10:00;00', 29.97)
        self.assertAlmostEqual(tc.time, 600)
        tc = DayuTimeCode('00:11:00;02', 29.97)
        self.assertAlmostEqual(tc.time, 660.0667334001)
        tc = DayuTimeCode('00:19:00;02', 29.97)
        self.assertAlmostEqual(tc.time, 1140.0667334001)
        tc = DayuTimeCode('01:00:00;01', 29.97)
        self.assertAlmostEqual(tc.time, 3600.033366700033)
        self.assertRaises(DayuTimeCodeValueError, DayuTimeCode, '00:01:00;00')
        self.assertRaises(DayuTimeCodeValueError, DayuTimeCode, '00:01:00;01')
        self.assertRaises(DayuTimeCodeValueError, DayuTimeCode, '00:02:00;00')
        self.assertRaises(DayuTimeCodeValueError, DayuTimeCode, '00:02:00;01')
        self.assertRaises(DayuTimeCodeValueError, DayuTimeCode, '00:03:00;00')
        self.assertRaises(DayuTimeCodeValueError, DayuTimeCode, '00:03:00;01')
        self.assertRaises(DayuTimeCodeValueError, DayuTimeCode, '00:04:00;00')
        self.assertRaises(DayuTimeCodeValueError, DayuTimeCode, '00:04:00;01')
        self.assertRaises(DayuTimeCodeValueError, DayuTimeCode, '00:05:00;00')
        self.assertRaises(DayuTimeCodeValueError, DayuTimeCode, '00:05:00;01')
        self.assertRaises(DayuTimeCodeValueError, DayuTimeCode, '00:06:00;00')
        self.assertRaises(DayuTimeCodeValueError, DayuTimeCode, '00:06:00;01')
        self.assertRaises(DayuTimeCodeValueError, DayuTimeCode, '00:07:00;00')
        self.assertRaises(DayuTimeCodeValueError, DayuTimeCode, '00:07:00;01')
        self.assertRaises(DayuTimeCodeValueError, DayuTimeCode, '00:08:00;00')
        self.assertRaises(DayuTimeCodeValueError, DayuTimeCode, '00:08:00;01')
        self.assertRaises(DayuTimeCodeValueError, DayuTimeCode, '00:09:00;00')
        self.assertRaises(DayuTimeCodeValueError, DayuTimeCode, '00:09:00;01')
        self.assertRaises(DayuTimeCodeValueError, DayuTimeCode, '00:11:00;00')
        self.assertRaises(DayuTimeCodeValueError, DayuTimeCode, '00:11:00;01')
        self.assertRaises(DayuTimeCodeValueError, DayuTimeCode, '00:59:00;00')
        self.assertRaises(DayuTimeCodeValueError, DayuTimeCode, '00:59:00;01')

        self.assertAlmostEqual(DayuTimeCode('01,000').time, 1)
        self.assertAlmostEqual(DayuTimeCode('1:01,000').time, 61)
        self.assertAlmostEqual(DayuTimeCode('00:00:00,000').time, 0)
        self.assertAlmostEqual(DayuTimeCode('00:00:00,500').time, 0.5)
        self.assertAlmostEqual(DayuTimeCode('01:02:03,500').time, 3723.5)
        self.assertRaises(DayuTimeCodeValueError, DayuTimeCode, '00:00:00,1023')
        self.assertRaises(DayuTimeCodeValueError, DayuTimeCode, ',1023')
        self.assertRaises(DayuTimeCodeValueError, DayuTimeCode, '01:02:03,')
        self.assertRaises(DayuTimeCodeValueError, DayuTimeCode, '25:02:03,')

        self.assertAlmostEqual(DayuTimeCode('01:000').time, 1)
        self.assertAlmostEqual(DayuTimeCode('1:01:000').time, 61)
        self.assertAlmostEqual(DayuTimeCode('02:11:01:000').time, 7861)
        self.assertAlmostEqual(DayuTimeCode('02:11:01:125').time, 7861.5)
        self.assertRaises(DayuTimeCodeValueError, DayuTimeCode, '01:251')
        self.assertRaises(DayuTimeCodeValueError, DayuTimeCode, '27:11:01:125')

        self.assertAlmostEqual(DayuTimeCode('1.0').time, 1)
        self.assertAlmostEqual(DayuTimeCode('1.1').time, 1.1)
        self.assertAlmostEqual(DayuTimeCode('00:00:00.04166666667').time, 0.04166666667)

        self.assertAlmostEqual(DayuTimeCode('0s').time, 0)
        self.assertAlmostEqual(DayuTimeCode('1s').time, 1)
        self.assertAlmostEqual(DayuTimeCode('108/274s').time, 0.3941605839)
        self.assertAlmostEqual(DayuTimeCode('99999999/1234s').time, 81037.2763371151)
        self.assertRaises(DayuTimeCodeValueError, DayuTimeCode, '123/456')
        self.assertRaises(DayuTimeCodeValueError, DayuTimeCode, 'aaa')
        self.assertRaises(DayuTimeCodeValueError, DayuTimeCode, '9862m')
        self.assertRaises(DayuTimeCodeValueError, DayuTimeCode, '-108/274s')

        self.assertAlmostEqual(DayuTimeCode([1, 24]), 1)
        self.assertAlmostEqual(DayuTimeCode([86400, 24]), 86400)
        self.assertAlmostEqual(DayuTimeCode([0, 24]), 0)
        self.assertAlmostEqual(DayuTimeCode([-24, 24]), -24)

        self.assertAlmostEqual(DayuTimeCode((1, 24)), 1)
        self.assertAlmostEqual(DayuTimeCode((86400, 24)), 86400)
        self.assertAlmostEqual(DayuTimeCode((0, 24)), 0)
        self.assertAlmostEqual(DayuTimeCode((-24, 24)), -24)

    def test_hour(self):
        self.assertEqual(DayuTimeCode(0).hour, 0)
        self.assertEqual(DayuTimeCode('1').hour, 0)
        self.assertEqual(DayuTimeCode('1:21').hour, 0)
        self.assertEqual(DayuTimeCode('03:01:21').hour, 0)
        self.assertEqual(DayuTimeCode('04:01:04:21').hour, 4)
        self.assertEqual(DayuTimeCode('23:01:04:21').hour, 23)
        self.assertEqual(DayuTimeCode(3456000).hour, 40)
        self.assertEqual(DayuTimeCode(-102).hour, 0)
        self.assertEqual(DayuTimeCode(-86400).hour, -1)

    def test_minute(self):
        self.assertEqual(DayuTimeCode(0).minute, 0)
        self.assertEqual(DayuTimeCode('1').minute, 0)
        self.assertEqual(DayuTimeCode('1:21').minute, 0)
        self.assertEqual(DayuTimeCode('03:01:21').minute, 3)
        self.assertEqual(DayuTimeCode('04:01:04:21').minute, 1)
        self.assertEqual(DayuTimeCode('23:01:04:21').minute, 1)
        self.assertEqual(DayuTimeCode(3456000).minute, 0)
        self.assertEqual(DayuTimeCode(-102234).minute, -10)
        self.assertEqual(DayuTimeCode(-86400).minute, 0)

    def test_second(self):
        self.assertEqual(DayuTimeCode(0).second, 0)
        self.assertEqual(DayuTimeCode('1').second, 0)
        self.assertEqual(DayuTimeCode('1:21').second, 1)
        self.assertEqual(DayuTimeCode('03:01:21').second, 1)
        self.assertEqual(DayuTimeCode('04:01:04:21').second, 4)
        self.assertEqual(DayuTimeCode('23:01:04:21').second, 4)
        self.assertEqual(DayuTimeCode(3456000).second, 0)
        self.assertEqual(DayuTimeCode(-102234).second, -59)
        self.assertEqual(DayuTimeCode(-86400).second, 0)

    def test_sub_frame(self):
        self.assertEqual(DayuTimeCode(0).sub_frame, 0)
        self.assertEqual(DayuTimeCode('1').sub_frame, 1)
        self.assertEqual(DayuTimeCode('1:21').sub_frame, 21)
        self.assertEqual(DayuTimeCode('03:01:21').sub_frame, 21)
        self.assertEqual(DayuTimeCode('04:01:04:22').sub_frame, 22)
        self.assertEqual(DayuTimeCode('23:01:04:4').sub_frame, 4)
        self.assertEqual(DayuTimeCode(3456000).sub_frame, 0)
        self.assertEqual(DayuTimeCode(-102234).sub_frame, 6)
        self.assertEqual(DayuTimeCode(-86400).sub_frame, 0)

    def test_frame(self):
        self.assertEqual(DayuTimeCode(0).frame(), 0)
        self.assertEqual(DayuTimeCode(1).frame(), 1)
        self.assertEqual(DayuTimeCode(102.3).frame(), 102.3)
        self.assertEqual(DayuTimeCode('00:12:22:7').frame(), 17815.0)

    def test_timecode(self):
        self.assertEqual(DayuTimeCode(0).timecode(), '00:00:00:00')
        self.assertEqual(DayuTimeCode(123123123123).timecode(), '12:08:50:03')
        tc = DayuTimeCode(123123123123)
        tc._HOUR_LOOP = False
        self.assertEqual(tc.timecode(), '1425036:08:50:03')
        tc = DayuTimeCode(-120)
        tc._HOUR_LOOP = False
        self.assertEqual(tc.timecode(), '-00:00:05:00')

        self.assertEqual(DayuTimeCode(1).timecode(), '00:00:00:01')
        self.assertEqual(DayuTimeCode('01:02:12:22').timecode(), '01:02:12:22')
        self.assertEqual(DayuTimeCode(-120).timecode(), '23:59:55:00')
        self.assertEqual(DayuTimeCode(119.96763430096763 * 29.97, fps=29.97).timecode(SMPTE_TIMECODE_DF), '00:01:59;29')
        self.assertEqual(DayuTimeCode(600 * 29.97, fps=29.97).timecode(SMPTE_TIMECODE_DF), '00:10:00;00')
        self.assertEqual(DayuTimeCode('00:00:00:00').timecode(SRT_TIMECODE), '00:00:00,000')
        self.assertEqual(DayuTimeCode('01:02:12:22').timecode(SRT_TIMECODE), '01:02:12,917')
        self.assertEqual(DayuTimeCode(-120).timecode(SRT_TIMECODE), '23:59:55,000')
        self.assertEqual(DayuTimeCode('00:00:00:00').timecode(DLP_TIMECODE), '00:00:00:000')
        self.assertEqual(DayuTimeCode('01:02:12:22').timecode(DLP_TIMECODE), '01:02:12:229')
        self.assertEqual(DayuTimeCode('00:00:00:00').timecode(FFMPEG_TIMECODE), '00:00:00.00')
        self.assertEqual(DayuTimeCode('01:02:12:22').timecode(FFMPEG_TIMECODE), '01:02:12.92')
        self.assertEqual(DayuTimeCode('00:00:00:00').timecode(FCPX_TIMECODE), '0s')
        self.assertEqual(DayuTimeCode('01:02:12:22').timecode(FCPX_TIMECODE), '8208770561037653/2199023255552s')

    def test__eq__(self):
        self.assertTrue(DayuTimeCode('00:00:00:00') == 0)
        self.assertTrue(DayuTimeCode(1) == 1)
        self.assertTrue(DayuTimeCode('00:59:59:23') == 86399)
        self.assertTrue(DayuTimeCode('23:59:59:23') == 2073599)
        self.assertTrue(DayuTimeCode(120) == 120)
        self.assertTrue(DayuTimeCode('00:12:22:7') == 17815.0)
        self.assertTrue(DayuTimeCode(-102234) == -102234)

    def test__lt__(self):
        self.assertLess(DayuTimeCode('00:00:00:00'), DayuTimeCode(1))
        self.assertLess(DayuTimeCode('00:00:10:00'), DayuTimeCode('00:00:12:00'))
        self.assertLess(DayuTimeCode('23:59:59:23'), DayuTimeCode(2073600))

    def test__le__(self):
        self.assertLessEqual(DayuTimeCode('00:00:00:00'), DayuTimeCode(1))
        self.assertLessEqual(DayuTimeCode('00:00:10:00'), DayuTimeCode('00:00:12:00'))
        self.assertLessEqual(DayuTimeCode('23:59:59:23'), DayuTimeCode(2073600))
        self.assertLessEqual(DayuTimeCode('23:59:59:23'), DayuTimeCode(2073599))

    def test__gt__(self):
        self.assertGreater(DayuTimeCode('00:00:00:00'), DayuTimeCode(-1))
        self.assertGreater(DayuTimeCode('00:00:10:00'), DayuTimeCode('00:00:09:00'))
        self.assertGreater(DayuTimeCode(2073600), DayuTimeCode('23:59:59:23'))

    def test__ge__(self):
        self.assertGreaterEqual(DayuTimeCode('00:00:00:00'), DayuTimeCode(-1))
        self.assertGreaterEqual(DayuTimeCode('00:00:10:00'), DayuTimeCode('00:00:09:00'))
        self.assertGreaterEqual(DayuTimeCode(2073600), DayuTimeCode('23:59:59:23'))
        self.assertGreaterEqual(DayuTimeCode(2073599), DayuTimeCode('23:59:59:23'))

    def test__float__(self):
        self.assertAlmostEqual(float(DayuTimeCode(0)), 0)
        self.assertAlmostEqual(float(DayuTimeCode(1)), 1)
        self.assertAlmostEqual(float(DayuTimeCode('00:00:00:00')), 0)
        self.assertAlmostEqual(float(DayuTimeCode('23:59:59:23')), 2073599)
        self.assertAlmostEqual(float(DayuTimeCode('00:00:00:02')), 2)

    def test___add__(self):
        self.assertAlmostEqual(DayuTimeCode(0) + DayuTimeCode(1), 1)
        self.assertAlmostEqual(DayuTimeCode(0) + DayuTimeCode(-120), -120)
        self.assertAlmostEqual(DayuTimeCode(100) + DayuTimeCode(200), 300)
        self.assertAlmostEqual(DayuTimeCode(100) + 1, 101)
        self.assertAlmostEqual(DayuTimeCode(-20) + 20, 0)
        self.assertAlmostEqual(DayuTimeCode('23:59:59:23') + 20, 2073619)
        self.assertIsInstance(DayuTimeCode('23:59:59:23') + 20, DayuTimeCode)

    def test___sub__(self):
        self.assertAlmostEqual(DayuTimeCode(1) - DayuTimeCode(1), 0)
        self.assertAlmostEqual(DayuTimeCode(0) - DayuTimeCode(-120), 120)
        self.assertAlmostEqual(DayuTimeCode(100) - DayuTimeCode(200), -100)
        self.assertAlmostEqual(DayuTimeCode(100) - 1, 99.0)
        self.assertAlmostEqual(DayuTimeCode(-20) - 20, -40)
        self.assertAlmostEqual(DayuTimeCode('23:59:59:23') - 20, 2073579)
        self.assertIsInstance(DayuTimeCode('23:59:59:23') - 20, DayuTimeCode)

    def test__mul__(self):
        self.assertAlmostEqual(DayuTimeCode(0) * 2, 0)
        self.assertAlmostEqual(DayuTimeCode(1) * 2, 2)
        self.assertAlmostEqual(DayuTimeCode(100) * (-2), -200)
        self.assertAlmostEqual(DayuTimeCode(-100) * 1.5, -150.0)
        self.assertIsInstance(DayuTimeCode('23:59:59:23') * 102.4, DayuTimeCode)

    def test_retime(self):
        pt = DayuTimeCode(1440)
        self.assertEqual(DayuTimeCode(1440).retime(pt, 2.0), 1440)
        self.assertEqual(DayuTimeCode(1440).retime(0, 2.0), 720)
        self.assertEqual(DayuTimeCode(1440).retime(-100, 0.5), 2980)
        self.assertEqual(DayuTimeCode(1440).retime(2880, 2), 2160)
        
    def test___copy__(self):
        a = DayuTimeCode(1440, fps=25)
        b = a
        a.fps = 50
        self.assertEqual(b.fps, 50)    
        c = copy.copy(a)
        c.fps = 25
        self.assertNotEqual(c.fps, a.fps)
        self.assertNotEqual(c.fps, b.fps)
