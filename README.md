# dayu_timecode

[![pypi](https://img.shields.io/badge/pypi-0.2-green.svg)](https://pypi.org/project/dayu-timecode/)
[![Python](https://img.shields.io/badge/python-2.7-blue.svg)]()
[![Build Status](https://travis-ci.org/phenom-films/dayu_timecode.svg?branch=master)](https://travis-ci.org/phenom-films/dayu_timecode)
[![GitHub license](https://img.shields.io/github/license/phenom-films/dayu_timecode.svg)](https://github.com/phenom-films/dayu_timecode/blob/master/LICENSE)


Timecode 的计算库。针对影视行业常见的各种timecode、frame 进行计算。有下面的特点：

* 支持SMPTE NDF、SMPTE DF、DLP、SRT、FFMPEG、FCPX 多种格式的timecode
* 目前支持到 fps=60 的高帧速率
* 支持hour loop 和 负数时间
* timecode、frame 之间自由转换
* 支持和其他常用的数字类型进行运算，无需转换（int、float、Fraction）


# 如何安装

直接使用pip 即可安装
```shell
pip install -U dayu_timecode
```

# DayuTimeCode 使用简介

```python
from dayu_timecode import DayuTimeCode

# 针对各种输入，进行初始化
smpte_ndf_tc = DayuTimeCode('01:02:03:12', fps=24.0)
smpte_df_tc = DayuTimeCode('01:09:00;02', fps=29.97)
srt_tc = DayuTimeCode('00:00:03,245', fps=25.0)
dlp_tc = DayuTimeCode('01:12:22:136', fps=24.0)
ffmpeg_tc = DayuTimeCode('00:02:12.24', fps=24.0)
fcpx_tc = DayuTimeCode('1/24s', fps=24.0)
frame_int_tc = DayuTimeCode(100, fps=25.0)
frame_long_tc = DayuTimeCode(86400.2, fps=24.0)
time_tc = DayuTimeCode([24, 3], fps=24.0)

# 时码、帧数转换
assert smpte_ndf_tc.timecode() == '01:02:03:12'
assert smpte_ndf_tc.frame() == 89364.00

# 得到时码中 小时、分钟、秒、帧数的分量
assert smpte_ndf_tc.hour == 1
assert smpte_ndf_tc.minute == 2
assert smpte_ndf_tc.second == 3
assert smpte_ndf_tc.sub_frame == 12

a = DayuTimeCode('01:02:03:12', fps=24.0)
b = DayuTimeCode(86400.2, fps=24.0)

# 加法、减法、乘法、除法
print a + b    # <DayuTimeCode>(02:02:03:12, 175764.20, 24.00)
print a - b    # <DayuTimeCode>(00:02:03:12, 2963.80, 24.00)
print a * 3    # <DayuTimeCode>(03:06:10:12, 268092.00, 24.00)
print a / 2    # <DayuTimeCode>(00:31:01:18, 44682.00, 24.00)

# 各种比较方式
print a == b
print a > b
print a >= b
print a < b
print a <= b
print a != b

# 类型转换
print float(a)
print int(a)

# 变速（指定一个起点，以及变速的速度）
start_tc = DayuTimeCode(0)
print a.retime(start_tc, 2.0)    # 表示从0 开始，两倍速播放后的timecode
```


# DayuTimeRange 使用简介

DayuTimeRange 由两个DayuTimeCode 组成的一个时间区域。

```python
# 初始化
start = DayuTimeCode(0)
end = DayuTimeCode(100)
time_range = DayuTimeRange(start, end)
# zero_length_range = DayuTimeRange(DayuTimeCode(10), DayuTimeCode(10))    # 会出错，因为start 和end 都是同一个时间

# 访问属性
print time_range.start  # 起点
print time_range.end  # 终点
print time_range.duration.frame()  # 获得 frame 长度
print len(time_range)  # 获得 frame 长度的另一种方法

# 加法、减法、乘法、除法
print time_range + 10  # 表示整个time_range 向右移动 10 frame
print time_range - 20  # 表示整个time_range 向左移动 20 frame
print time_range * 2  # 表示整个time_range 起点不动，长度变成原来的 2 倍
print time_range / 3  # 表示整个time_range 起点不动，长度变成原来的 三分之一

# 处理handle
time_range.handle(10, 10)  # 表示time_range 的start 向左增加 10 frame，end 向右增加 10 frame

# 切镜头处理
cut_point = DayuTimeCode(20)
print time_range.cut(cut_point)  # 得到两个区域 (0 - 20), (20 - 100)

# 判断timecode 或者一个time range 是否在当前timerange 的内部
sample_tc = DayuTimeCode(20)
sample_time_range = DayuTimeRange(DayuTimeCode(30), DayuTimeCode(70))
assert sample_tc in time_range
assert sample_time_range in time_range

# 两个DayuTimeRange 之间的交集、并集、差异 运算
a = DayuTimeRange(DayuTimeCode(0), DayuTimeCode(100))
b = DayuTimeRange(DayuTimeCode(50), DayuTimeCode(150))
print a & b  # 二者之间交叠的部分 (50 - 100)
print a | b  # 二者的并集运算 （0 - 150）
print a ^ b  # 二者的差异运算  (0 - 50), (100 - 150)

# 遍历time range 内的所有时码
for tc in time_range:
    print tc  # 会逐一打印 从 DayuTimeCode(0) ~ DayuTimeCode(99)
```