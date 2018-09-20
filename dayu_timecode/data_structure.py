#!/usr/bin/env python
# -*- encoding: utf-8 -*-

__author__ = 'andyguo'

from collections import namedtuple

# 用来表示变速的数据结构。其中.org_range 表示原始需要的TimeRange，.speed_range 表示变速后的TimeRange
# 两个TimeRange 之间就是形成了变速的映射关系
SpeedMap = namedtuple('SpeedMap', ('org_range', 'speed_range'))
