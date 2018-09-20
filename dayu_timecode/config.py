#!/usr/bin/env python
# -*- encoding: utf-8 -*-

__author__ = 'andyguo'

import re

SMPTE_REGEX_NDF = re.compile(r'^(?:(?:(?:([01]?\d|2[0-3]|\d{3}):)?([0-5]?\d):)?([0-5]?\d):)?([0-5]?\d)$')
SMPTE_REGEX_DF = re.compile(r'^(?:(?:(?:([01]?\d|2[0-3]|\d{3}):)?([0-5]?\d):)?([0-5]?\d);)?([0-5]?\d)$')
SRT_REGEX = re.compile(r'^(?:(?:(?:([01]?\d|2[0-3]|\d{3}):)?([0-5]?\d):)?([0-5]?\d),)?(\d\d\d)$')
DLP_REGEX = re.compile(r'^(?:(?:(?:([01]?\d|2[0-3]|\d{3}):)?([0-5]?\d):)?([0-5]?\d):)?([0-2][0-4]\d)$')
FFMPEG_REGEX = re.compile(r'^(?:(?:(?:([01]?\d|2[0-3]|\d{3}):)?([0-5]?\d):)?([0-5]?\d)\.)?(\d?\d+)$')
FCPX_REGEX = re.compile(r'^(\d+)[/]?(\d+)?s$')

SMPTE_TIMECODE_NDF = 'SMPTE_TIMECODE_NDF'
SMPTE_TIMECODE_DF = 'SMPTE_TIMECODE_DF'
SRT_TIMECODE = 'SRT_TIMECODE'
DLP_TIMECODE = 'DLP_TIMECODE'
FFMPEG_TIMECODE = 'FFMPEG_TIMECODE'
FCPX_TIMECODE = 'FCPX_TIMECODE'
