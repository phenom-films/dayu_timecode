#!/usr/bin/env python
# -*- encoding: utf-8 -*-

__author__ = 'andyguo'

from fractions import Fraction
from config import *
from dispath import InstanceMethodDispatch
from data_structure import SpeedMap
from error import DayuTimeCodeValueError


class DayuTimeCode(object):
    _HOUR_LOOP = True
    _NEGATIVE_TIMECODE = False

    def __new__(cls, value, fps=24.0):
        if isinstance(value, DayuTimeCode):
            return value
        else:
            return super(DayuTimeCode, cls).__new__(cls, value, fps=fps)

    @InstanceMethodDispatch.dispatch()
    def __init__(self, value, fps):
        pass

    @InstanceMethodDispatch.register('__init__', str)
    def _(self, string_value, fps=24.0):
        self.fps = float(fps)
        if SMPTE_REGEX_NDF.match(string_value):
            my_tc = [int(x) if x else 0 for x in SMPTE_REGEX_NDF.match(string_value).groups()]
            frame_count = my_tc[0] * 3600 + my_tc[1] * 60 + my_tc[2] + my_tc[3] / self.fps
            self.time = Fraction(frame_count)
        elif SMPTE_REGEX_DF.match(string_value):
            my_tc = [int(x) if x else 0 for x in SMPTE_REGEX_DF.match(string_value).groups()]
            if my_tc[1] % 10 != 0 and my_tc[3] in (0, 1):
                raise DayuTimeCodeValueError

            frame_count = my_tc[0] * 3600 + my_tc[1] * 60 + my_tc[2] + my_tc[3] / self.fps
            self.time = Fraction(frame_count)
        elif SRT_REGEX.match(string_value):
            my_tc = [int(x) if x else 0 for x in SRT_REGEX.match(string_value).groups()]
            frame_count = my_tc[0] * 3600 + my_tc[1] * 60 + my_tc[2] + my_tc[3] / 1000.0
            self.time = Fraction(frame_count)
        elif DLP_REGEX.match(string_value):
            my_tc = [int(x) if x else 0 for x in DLP_REGEX.match(string_value).groups()]
            frame_count = my_tc[0] * 3600 + my_tc[1] * 60 + my_tc[2] + my_tc[3] / 250.0
            self.time = Fraction(frame_count)
        elif FFMPEG_REGEX.match(string_value):
            my_tc = [x if x else 0 for x in FFMPEG_REGEX.match(string_value).groups()]
            frame_count = int(my_tc[0]) * 3600 + int(my_tc[1]) * 60 + int(my_tc[2]) + float('0.{}'.format(my_tc[3]))
            self.time = Fraction(frame_count)
        elif FCPX_REGEX.match(string_value):
            my_tc = [int(x) if x else 1 for x in FCPX_REGEX.match(string_value).groups()]
            self.time = Fraction(my_tc[0], my_tc[1])
        else:
            raise DayuTimeCodeValueError

    @InstanceMethodDispatch.register('__init__', int)
    def _(self, frame_count, fps=24.0):
        self.fps = float(fps)
        self.time = Fraction.from_float(frame_count / self.fps)

    @InstanceMethodDispatch.register('__init__', float)
    def _(self, float_value, fps=24.0):
        self.fps = float(fps)
        self.time = Fraction.from_float(float_value / self.fps)

    @InstanceMethodDispatch.register('__init__', Fraction)
    def _(self, fraction_value, fps=24.0):
        self.fps = float(fps)
        self.time = fraction_value

    @InstanceMethodDispatch.register('__init__', tuple)
    def _(self, tuple_value, fps=24.0):
        self.fps = fps
        self.time = Fraction(int(tuple_value[0]), int(tuple_value[1]))

    @InstanceMethodDispatch.register('__init__', list)
    def _(self, list_value, fps=24.0):
        self.fps = fps
        self.time = Fraction(int(list_value[0]), int(list_value[1]))

    @property
    def hour(self):
        return int(self.time / 3600)

    @property
    def minute(self):
        hh = int(self.time / 3600)
        return int((self.time - hh * 3600) / 60)

    @property
    def second(self):
        hh = int(self.time / 3600)
        mm = int((self.time - hh * 3600) / 60)
        return int(self.time - hh * 3600 - mm * 60)

    @property
    def sub_frame(self):
        hh = int(self.time / 3600)
        mm = (self.time - hh * 3600) // 60
        ss = round((self.time - hh * 3600 - mm * 60) // 1, 0)
        ff = float(self.time - hh * 3600 - mm * 60 - ss)
        return int(round(ff * self.fps, 0))

    def __get_hhmmssff(self):
        if self._HOUR_LOOP:
            sign = 1
            if self.time < 0:
                temp_time = self.time + Fraction.from_float(int(self.time / 3600.0) + 24 * 3600.0)
            else:
                temp_time = self.time - Fraction.from_float(int(self.time / (3600.0 * 24)) * 24 * 3600.0)
        else:
            sign = 1 if self.time >= 0 else -1
            temp_time = abs(self.time)

        hh = int(temp_time / 3600)
        mm = (temp_time - hh * 3600) // 60
        ss = round((temp_time - hh * 3600 - mm * 60) // 1, 0)
        ff = float(temp_time - hh * 3600 - mm * 60 - ss)
        hh = hh if hh >= 0 else hh + abs(hh) * 24
        return sign, int(hh), int(mm), int(ss), ff

    def frame(self):
        return round(float(self.time * self.fps), 7)

    def _convert_to_SMPTE_TIMECODE_NDF(self):
        sign, hh, mm, ss, ff = self.__get_hhmmssff()
        return '{}{:02d}:{:02d}:{:02d}:{:02d}'.format('' if sign > 0 else '-',
                                                      hh, mm, ss, int(round(ff * self.fps, 0)))

    def _convert_to_SMPTE_TIMECODE_DF(self):
        sign, hh, mm, ss, ff = self.__get_hhmmssff()
        return '{:02d}:{:02d}:{:02d};{:02d}'.format(hh, mm, ss, int(round(ff * self.fps, 0)))

    def _convert_to_SRT_TIMECODE(self):
        sign, hh, mm, ss, ff = self.__get_hhmmssff()
        return '{:02d}:{:02d}:{:02d},{:03d}'.format(hh, mm, ss, int(round(ff * 1000.0, 0)))

    def _convert_to_DLP_TIMECODE(self):
        sign, hh, mm, ss, ff = self.__get_hhmmssff()
        return '{:02d}:{:02d}:{:02d}:{:03d}'.format(hh, mm, ss, int(round(ff * 250.0, 0)))

    def _convert_to_FFMPEG_TIMECODE(self):
        sign, hh, mm, ss, ff = self.__get_hhmmssff()
        return '{:02d}:{:02d}:{:02d}.{:02d}'.format(hh, mm, ss, int(round(ff * 100.0, 0)))

    def _convert_to_FCPX_TIMECODE(self):
        return '{numerator}{denominator}s'.format(numerator=self.time.numerator,
                                                  denominator='' if float(self.time).is_integer() else '/{}'.format(
                                                          self.time.denominator))

    def timecode(self, type='SMPTE_TIMECODE_NDF'):
        func = getattr(self, '_convert_to_{}'.format(type), None)
        if func:
            return func()

    def __repr__(self):
        return '<DayuTimeCode>({}, {:.02f}, {:.02f})'.format(self.timecode(), self.frame(), self.fps)

    def __abs__(self):
        self.time = abs(self.time)
        return self

    def __add__(self, other):
        return DayuTimeCode(self.time + DayuTimeCode(other, self.fps).time, fps=self.fps)

    def __iadd__(self, other):
        self.time += DayuTimeCode(other, self.fps).time
        return self

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        return DayuTimeCode(self.time - DayuTimeCode(other, self.fps).time, fps=self.fps)

    def __isub__(self, other):
        self.time -= DayuTimeCode(other, self.fps).time
        return self

    def __rsub__(self, other):
        return self.__sub__(other)

    def __mul__(self, other):
        return DayuTimeCode(self.time * float(other) * self.fps, fps=self.fps)

    def __imul__(self, other):
        self.time *= DayuTimeCode(other, self.fps).time
        return self

    def __rmul__(self, other):
        return self.__mul__(other)

    def __div__(self, other):
        return DayuTimeCode(self.time / float(other) * self.fps, fps=self.fps)

    def __idiv__(self, other):
        self.time /= DayuTimeCode(other, self.fps)
        return self

    def __rdiv__(self, other):
        return self

    def __eq__(self, other):
        if isinstance(other, DayuTimeCode):
            return self.time == other.time
        return round(self.time * self.fps, 7) == other

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        if isinstance(other, DayuTimeCode):
            return self.time < other.time
        return round(self.time * self.fps, 7) < other

    def __gt__(self, other):
        if isinstance(other, DayuTimeCode):
            return self.time > other.time
        return round(self.time * self.fps, 7) > other

    def __le__(self, other):
        if isinstance(other, DayuTimeCode):
            return self.time <= other.time
        return round(self.time * self.fps, 7) <= other

    def __ge__(self, other):
        if isinstance(other, DayuTimeCode):
            return self.time >= other.time
        return round(self.time * self.fps, 7) >= other

    def __float__(self):
        return float(self.time * self.fps)

    def __int__(self):
        return int(self.time * self.fps)

    def __neg__(self):
        self.time = -self.time
        return self

    def retime(self, point, retime):
        '''
        基于某个起点，当前时码进行变速。
        :param point: Timecode 类型的对象
        :param retime: float，表示变速的百分比。1.0 表示不变速
        :return: Timecode 对象，变速后的Timecode
        '''
        return DayuTimeCode(point + (self - point) / float(retime), fps=self.fps)
