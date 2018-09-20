#!/usr/bin/env python
# -*- encoding: utf-8 -*-

__author__ = 'andyguo'

import exceptions


class DayuTimeCodeValueError(exceptions.ValueError):
    pass


class DayuTimeRangeValueError(exceptions.ValueError):
    pass


class DayuTimeRangeFpsNotIdenticalError(exceptions.ValueError):
    pass


class DayuTimeRangeOperationError(exceptions.ValueError):
    pass


class DayuTimeRangeOutOfRange(exceptions.ValueError):
    pass
