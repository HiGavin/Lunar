# lunar.py
# 2015/02/27  罗兵  原作者 公历生成农历，年干支、日干支
# 2019/07/14  张高尉  增加了月干支，时干支，五行分析
import datetime
import sys


class Lunar(object):
    # ******************************************************************************
    # 下面为阴历计算所需的数据,为节省存储空间,所以采用下面比较变态的存储方法.
    # ******************************************************************************
    # 数组g_lunar_month_day存入阴历1901年到2050年每年中的月天数信息，
    # 阴历每月只能是29或30天，一年用12（或13）个二进制位表示，对应位为1表30天，否则为29天
    g_lunar_month_day = [
        0x4ae0, 0xa570, 0x5268, 0xd260, 0xd950, 0x6aa8, 0x56a0, 0x9ad0, 0x4ae8, 0x4ae0,  # 1910
        0xa4d8, 0xa4d0, 0xd250, 0xd548, 0xb550, 0x56a0, 0x96d0, 0x95b0, 0x49b8, 0x49b0,  # 1920
        0xa4b0, 0xb258, 0x6a50, 0x6d40, 0xada8, 0x2b60, 0x9570, 0x4978, 0x4970, 0x64b0,  # 1930
        0xd4a0, 0xea50, 0x6d48, 0x5ad0, 0x2b60, 0x9370, 0x92e0, 0xc968, 0xc950, 0xd4a0,  # 1940
        0xda50, 0xb550, 0x56a0, 0xaad8, 0x25d0, 0x92d0, 0xc958, 0xa950, 0xb4a8, 0x6ca0,  # 1950
        0xb550, 0x55a8, 0x4da0, 0xa5b0, 0x52b8, 0x52b0, 0xa950, 0xe950, 0x6aa0, 0xad50,  # 1960
        0xab50, 0x4b60, 0xa570, 0xa570, 0x5260, 0xe930, 0xd950, 0x5aa8, 0x56a0, 0x96d0,  # 1970
        0x4ae8, 0x4ad0, 0xa4d0, 0xd268, 0xd250, 0xd528, 0xb540, 0xb6a0, 0x96d0, 0x95b0,  # 1980
        0x49b0, 0xa4b8, 0xa4b0, 0xb258, 0x6a50, 0x6d40, 0xada0, 0xab60, 0x9370, 0x4978,  # 1990
        0x4970, 0x64b0, 0x6a50, 0xea50, 0x6b28, 0x5ac0, 0xab60, 0x9368, 0x92e0, 0xc960,  # 2000
        0xd4a8, 0xd4a0, 0xda50, 0x5aa8, 0x56a0, 0xaad8, 0x25d0, 0x92d0, 0xc958, 0xa950,  # 2010
        0xb4a0, 0xb550, 0xb550, 0x55a8, 0x4ba0, 0xa5b0, 0x52b8, 0x52b0, 0xa930, 0x74a8,  # 2020
        0x6aa0, 0xad50, 0x4da8, 0x4b60, 0x9570, 0xa4e0, 0xd260, 0xe930, 0xd530, 0x5aa0,  # 2030
        0x6b50, 0x96d0, 0x4ae8, 0x4ad0, 0xa4d0, 0xd258, 0xd250, 0xd520, 0xdaa0, 0xb5a0,  # 2040
        0x56d0, 0x4ad8, 0x49b0, 0xa4b8, 0xa4b0, 0xaa50, 0xb528, 0x6d20, 0xada0, 0x55b0,  # 2050
    ]

    # 数组gLanarMonth存放阴历1901年到2050年闰月的月份，如没有则为0，每字节存两年
    g_lunar_month = [
        0x00, 0x50, 0x04, 0x00, 0x20,  # 1910
        0x60, 0x05, 0x00, 0x20, 0x70,  # 1920
        0x05, 0x00, 0x40, 0x02, 0x06,  # 1930
        0x00, 0x50, 0x03, 0x07, 0x00,  # 1940
        0x60, 0x04, 0x00, 0x20, 0x70,  # 1950
        0x05, 0x00, 0x30, 0x80, 0x06,  # 1960
        0x00, 0x40, 0x03, 0x07, 0x00,  # 1970
        0x50, 0x04, 0x08, 0x00, 0x60,  # 1980
        0x04, 0x0a, 0x00, 0x60, 0x05,  # 1990
        0x00, 0x30, 0x80, 0x05, 0x00,  # 2000
        0x40, 0x02, 0x07, 0x00, 0x50,  # 2010
        0x04, 0x09, 0x00, 0x60, 0x04,  # 2020
        0x00, 0x20, 0x60, 0x05, 0x00,  # 2030
        0x30, 0xb0, 0x06, 0x00, 0x50,  # 2040
        0x02, 0x07, 0x00, 0x50, 0x03  # 2050
    ]

    START_YEAR = 1901

    # 天干
    gan = '甲乙丙丁戊己庚辛壬癸'
    # 地支
    zhi = '子丑寅卯辰巳午未申酉戌亥'
    # 生肖
    xiao = '鼠牛虎兔龙蛇马羊猴鸡狗猪'
    # 月份
    lm = '正二三四五六七八九十冬腊'
    # 日份
    ld = '初一初二初三初四初五初六初七初八初九初十十一十二十三十四十五十六十七十八十九二十廿一廿二廿三廿四廿五廿六廿七廿八廿九三十'
    # 节气
    jie = '小寒大寒立春雨水惊蛰春分清明谷雨立夏小满芒种夏至小暑大暑立秋处暑白露秋分寒露霜降立冬小雪大雪冬至'
    # 节气划分农历干支月
    jie_qi_odd = "立春惊蛰清明立夏芒种小暑立秋白露寒露立冬大雪小寒"  # 节气节点，如立春-惊蛰是正月，两个节气一个月
    # 节气对应农历干支月
    jie_qi_month = {
        "立春": [0, "寅"],
        "惊蛰": [1, "卯"],
        "清明": [2, "辰"],
        "立夏": [3, "巳"],
        "芒种": [4, "午"],
        "小暑": [5, "未"],
        "立秋": [6, "申"],
        "白露": [7, "酉"],
        "寒露": [8, "戌"],
        "立冬": [9, "亥"],
        "大雪": [10, "子"],
        "小寒": [11, "丑"],
    }
    gz_wu_xing = {
        '甲': '木',
        '乙': '木',
        '丙': '火',
        '丁': '火',
        '戊': '土',
        '己': '土',
        '庚': '金',
        '辛': '金',
        '壬': '水',
        '癸': '水',
        '子': '水',
        '丑': '土',
        '寅': '木',
        '卯': '木',
        '辰': '土',
        '巳': '火',
        '午': '火',
        '未': '土',
        '申': '金',
        '酉': '金',
        '戌': '土',
        '亥': '水',
    }
    nian_ben_ming = {
        '甲子': '海中金命',
        '乙丑': '海中金命',
        '丙寅': '炉中火命',
        '丁卯': '炉中火命',
        '戊辰': '大林木命',
        '己巳': '大林木命',
        '庚午': '路旁土命',
        '辛未': '路旁土命',
        '壬申': '剑锋金命',
        '癸酉': '剑锋金命',
        '甲戌': '山头火命',
        '乙亥': '山头火命',
        '丙子': '涧下水命',
        '丁丑': '涧下水命',
        '戊寅': '城头土命',
        '己卯': '城头土命',
        '庚辰': '白蜡金命',
        '辛巳': '白蜡金命',
        '壬午': '杨柳木命',
        '癸未': '杨柳木命',
        '甲申': '泉中水命',
        '乙酉': '泉中水命',
        '丙戌': '屋上土命',
        '丁亥': '屋上土命',
        '戊子': '霹雳火命',
        '己丑': '霹雳火命',
        '庚寅': '松柏木命',
        '辛卯': '松柏木命',
        '壬辰': '长流水命',
        '癸巳': '长流水命',
        '甲午': '砂石金命',
        '乙未': '砂石金命',
        '丙申': '山下火命',
        '丁酉': '山下火命',
        '戊戌': '平地木命',
        '己亥': '平地木命',
        '庚子': '壁上土命',
        '辛丑': '壁上土命',
        '壬寅': '金薄金命',
        '癸卯': '金薄金命',
        '甲辰': '覆灯火命',
        '乙巳': '覆灯火命',
        '丙午': '天河水命',
        '丁未': '天河水命',
        '戊申': '大驿土命',
        '己酉': '大驿土命',
        '庚戌': '钗环金命',
        '辛亥': '钗环金命',
        '壬子': '桑柘木命',
        '癸丑': '桑柘木命',
        '甲寅': '大溪水命',
        '已卯': '大溪水命',
        '丙辰': '沙中土命',
        '丁巳': '沙中土命',
        '戊午': '天上火命',
        '己未': '天上火命',
        '庚申': '石榴木命',
        '辛酉': '石榴木命',
        '壬戌': '大海水命',
        '癸亥': '大海水命',
    }

    def __init__(self, dt=None):
        """ 初始化：参数为datetime.datetime类实例，默认当前时间  """
        self.localtime = dt if dt else datetime.datetime.today()
        self.gz_year_value = ""
        self.ln_month_value = ""
        self.wu_xing = ""

    def sx_year(self):  # 返回生肖年
        ct = self.localtime  # 取当前时间
        year = self.ln_year() - 3 - 1  # 农历年份减3 （说明：补减1）
        year = year % 12  # 模12，得到地支数
        return self.xiao[year]

    def gz_year(self):  # 返回干支纪年
        ct = self.localtime  # 取当前时间
        year = self.ln_year() - 3 - 1  # 农历年份减3 （说明：补减1）
        G = year % 10  # 模10，得到天干数
        Z = year % 12  # 模12，得到地支数
        self.gz_year_value = self.gan[G] + self.zhi[Z]
        return self.gz_year_value

    def gz_month(self):  # 返回干支纪月（原作者未实现）
        """
        干支纪月的计算规则较为复杂，是本人在前人的基础上实现的，填补了空白。
        1、首先判断当前日期所处的节气范围，
        2、特别要考虑年数是否需要增减，以立春为界，如正月尚未立春的日子年数减一，
        3、月的天干公式 （年干序号 * 2 + 月数） % 10 ，其中 0 表示最后一个天干，
        4、月的地支是固定的，查表可得。
        :return:
        """
        ct = self.localtime  # 取当前时间
        jie_qi = self.ln_jie()
        nl_month_val = self.ln_month()
        if len(jie_qi) > 0 and jie_qi in self.jie_qi_odd:   # 如果恰好是节气当日
            if self.jie_qi_month[jie_qi][0] == 0 and nl_month_val == 12:  #
                year = self.ln_year() - 3  # 虽然农历已经是腊月，但是已经立春， 所以年加一
                G = year % 10  # 模10，得到天干数
                Z = year % 12  # 模12，得到地支数
                nl_year = self.gan[G] + self.zhi[Z]
                nl_month = 0
            else:
                nl_year = self.gz_year_value  # 干支纪年
                nl_month = self.jie_qi_month[jie_qi][0]  # 计算出干支纪月
        else:      # 如果不是节气日，则循环判断后一个分月节气是什么
            nl_year = self.gz_year_value
            nl_month = 0
            for i in range(-1, -40, -1):
                var_days = ct + datetime.timedelta(days=i)
                jie_qi = self.nl_jie(var_days)
                if len(jie_qi) > 0 and jie_qi in self.jie_qi_odd:
                    if self.jie_qi_month[jie_qi][0] > 0:
                        nl_month = self.jie_qi_month[jie_qi][0]
                    elif self.jie_qi_month[jie_qi][0] == 0 and nl_month_val == 12:   #
                        year = self.ln_year() - 3    # 虽然农历已经是腊月，但是已经立春， 所以年加一
                        G = year % 10  # 模10，得到天干数
                        Z = year % 12  # 模12，得到地支数
                        nl_year = self.gan[G] + self.zhi[Z]
                        nl_month = 0
                    else:
                        nl_month = 0
                    break
        gan_str = self.gan
        # print(nl_year[0])
        month_num = (gan_str.find(nl_year[0])+1) * 2 + nl_month + 1
        M = month_num % 10
        if M == 0:
            M = 10
        gz_month = self.gan[M-1] + self.jie_qi_month[jie_qi][1]
        return gz_month

    def gz_day(self):  # 返回干支纪日
        ct = self.localtime  # 取当前时间
        C = ct.year // 100  # 取世纪数，减一
        y = ct.year % 100  # 取年份后两位（若为1月、2月则当前年份减一）
        y = y - 1 if ct.month == 1 or ct.month == 2 else y
        M = ct.month  # 取月份（若为1月、2月则分别按13、14来计算）
        M = M + 12 if ct.month == 1 or ct.month == 2 else M
        d = ct.day  # 取日数
        i = 0 if ct.month % 2 == 1 else 6  # 取i （奇数月i=0，偶数月i=6）

        # 下面两个是网上的公式
        # http://baike.baidu.com/link?url=MbTKmhrTHTOAz735gi37tEtwd29zqE9GJ92cZQZd0X8uFO5XgmyMKQru6aetzcGadqekzKd3nZHVS99rewya6q
        # 计算干（说明：补减1）
        G = 4 * C + C // 4 + 5 * y + y // 4 + 3 * (M + 1) // 5 + d - 3 - 1
        G = G % 10
        # 计算支（说明：补减1）
        Z = 8 * C + C // 4 + 5 * y + y // 4 + 3 * (M + 1) // 5 + d + 7 + i - 1
        Z = Z % 12

        # 返回 干支纪日
        return self.gan[G] + self.zhi[Z]

    def gz_hour(self):  # 返回干支纪时（时辰）
        """
        原作者计算的时干支，实际上只返回了时辰的地支，缺少天干；
        我补充了天干的计算，公式皆为原创
        时干数 = ((日干 % 5)*2 + 时辰 -2) % 10
        :return:
        """
        ct = self.localtime  # 取当前时间
        # 计算支
        Z = round((ct.hour / 2) + 0.1) % 12  # 之所以加0.1是因为round的bug!!
        gz_day_value = self.gz_day()
        gz_day_num = self.gan.find(gz_day_value[0]) + 1
        gz_day_yu = gz_day_num % 5
        hour_num = Z + 1
        if gz_day_yu == 0:
            gz_day_yu = 5
        gz_hour_num = (gz_day_yu * 2 - 1 + hour_num-1) % 10
        if gz_hour_num == 0:
            gz_hour_num = 10
        # 返回 干支纪时（时辰）
        return self.gan[gz_hour_num-1] + self.zhi[Z]

    def ln_year(self):  # 返回农历年
        year, _, _ = self.ln_date()
        return year

    def ln_month(self):  # 返回农历月
        _, month, _ = self.ln_date()
        self.ln_month_value = month
        return month

    def ln_day(self):  # 返回农历日
        _, _, day = self.ln_date()
        return day

    def ln_date(self):  # 返回农历日期整数元组（年、月、日）（查表法）
        delta_days = self._date_diff()

        # 阳历1901年2月19日为阴历1901年正月初一
        # 阳历1901年1月1日到2月19日共有49天
        if delta_days < 49:
            year = self.START_YEAR - 1
            if delta_days < 19:
                month = 11
                day = 11 + delta_days
            else:
                month = 12
                day = delta_days - 18
            return year, month, day

        # 下面从阴历1901年正月初一算起
        delta_days -= 49
        year, month, day = self.START_YEAR, 1, 1
        # 计算年
        tmp = self._lunar_year_days(year)
        while delta_days >= tmp:
            delta_days -= tmp
            year += 1
            tmp = self._lunar_year_days(year)

        # 计算月
        (foo, tmp) = self._lunar_month_days(year, month)
        while delta_days >= tmp:
            delta_days -= tmp
            if month == self._get_leap_month(year):
                (tmp, foo) = self._lunar_month_days(year, month)
                if delta_days < tmp:
                    return 0, 0, 0
                delta_days -= tmp
            month += 1
            (foo, tmp) = self._lunar_month_days(year, month)

        # 计算日
        day += delta_days
        return year, month, day

    def ln_date_str(self):  # 返回农历日期字符串，形如：农历正月初九
        year, month, day = self.ln_date()
        return '农历{}年 {}月 {}'.format(year, self.lm[month - 1], self.ld[(day - 1) * 2:day * 2])

    def ln_jie(self):  # 返回农历节气
        ct = self.localtime  # 取当前时间
        year = ct.year
        for i in range(24):
            # 因为两个都是浮点数，不能用相等表示
            delta = self._julian_day() - self._julian_day_of_ln_jie(year, i)
            if -.5 <= delta <= .5:
                return self.jie[i * 2:(i + 1) * 2]
        return ''

    def nl_jie(self,dt):
        year = dt.year
        for i in range(24):
            # 因为两个都是浮点数，不能用相等表示
            delta = self.rulian_day(dt) - self._julian_day_of_ln_jie(year, i)
            if -.5 <= delta <= .5:
                return self.jie[i * 2:(i + 1) * 2]
        return ''

    # 显示日历
    def calendar(self):
        pass

    #######################################################
    #            下面皆为私有函数
    #######################################################

    def _date_diff(self):
        """ 返回基于1901/01/01日差数 """
        return (self.localtime - datetime.datetime(1901, 1, 1)).days

    def _get_leap_month(self, lunar_year):
        flag = self.g_lunar_month[(lunar_year - self.START_YEAR) // 2]
        if (lunar_year - self.START_YEAR) % 2:
            return flag & 0x0f
        else:
            return flag >> 4

    def _lunar_month_days(self, lunar_year, lunar_month):
        if lunar_year < self.START_YEAR:
            return 30

        high, low = 0, 29
        iBit = 16 - lunar_month

        if lunar_month > self._get_leap_month(lunar_year) and self._get_leap_month(lunar_year):
            iBit -= 1

        if self.g_lunar_month_day[lunar_year - self.START_YEAR] & (1 << iBit):
            low += 1

        if lunar_month == self._get_leap_month(lunar_year):
            if self.g_lunar_month_day[lunar_year - self.START_YEAR] & (1 << (iBit - 1)):
                high = 30
            else:
                high = 29

        return high, low

    def _lunar_year_days(self, year):
        days = 0
        for i in range(1, 13):
            (high, low) = self._lunar_month_days(year, i)
            days += high
            days += low
        return days

    # 返回指定公历日期的儒略日（http://blog.csdn.net/orbit/article/details/9210413）
    def _julian_day(self):
        ct = self.localtime  # 取当前时间
        year = ct.year
        month = ct.month
        day = ct.day

        if month <= 2:
            month += 12
            year -= 1

        B = year / 100
        B = 2 - B + year / 400

        dd = day + 0.5000115740  # 本日12:00后才是儒略日的开始(过一秒钟)*/
        return int(365.25 * (year + 4716) + 0.01) + int(30.60001 * (month + 1)) + dd + B - 1524.5

    def rulian_day(self, dt):   # 重写_julian_day 函数，变成可以传参的函数
        year = dt.year
        month = dt.month
        day = dt.day
        if month <= 2:
            month += 12
            year -= 1

        B = year / 100
        B = 2 - B + year / 400

        dd = day + 0.5000115740  # 本日12:00后才是儒略日的开始(过一秒钟)*/
        return int(365.25 * (year + 4716) + 0.01) + int(30.60001 * (month + 1)) + dd + B - 1524.5

        # 返回指定年份的节气的儒略日数（http://blog.csdn.net/orbit/article/details/9210413）
    def _julian_day_of_ln_jie(self, year, st):
        s_stAccInfo = [
            0.00, 1272494.40, 2548020.60, 3830143.80, 5120226.60, 6420865.80,
            7732018.80, 9055272.60, 10388958.00, 11733065.40, 13084292.40, 14441592.00,
            15800560.80, 17159347.20, 18513766.20, 19862002.20, 21201005.40, 22529659.80,
            23846845.20, 25152606.00, 26447687.40, 27733451.40, 29011921.20, 30285477.60]

        # 已知1900年小寒时刻为1月6日02:05:00
        base1900_SlightColdJD = 2415025.5868055555

        if (st < 0) or (st > 24):
            return 0.0

        stJd = 365.24219878 * (year - 1900) + s_stAccInfo[st] / 86400.0

        return base1900_SlightColdJD + stJd

    #######################################################
    #            下面为五行分析
    #######################################################

    def gz_to_wu_xing(self, gz_str):
        if len(gz_str) > 0:
            wu_xing = ""
            for gz in list(gz_str):
                wu_xing = wu_xing + self.gz_wu_xing[gz]
            return wu_xing
        else:
            return ""

    def gen_wu_xing(self):
        gz_year = self.gz_year()
        gz_month = self.gz_month()
        gz_day = self.gz_day()
        gz_hour = self.gz_hour()
        gz_list = [gz_year, gz_month, gz_day, gz_hour]
        wu_xing_str = ""
        for g in gz_list:
            wu_xing_str = wu_xing_str + self.gz_to_wu_xing(g)
        count = {}
        for i in wu_xing_str:
            if i not in count:
                count[i] = 1
            else:
                count[i] += 1
        return count

    def wu_xing_lack(self):
        wu_xing = ["金", "木", "水", "火", "土"]
        gen_wu_xing = self.gen_wu_xing()
        ben_ming_wu_xing = self.nian_ben_ming[self.gz_year()][-2]
        if ben_ming_wu_xing in gen_wu_xing.keys():
            gen_wu_xing[ben_ming_wu_xing] += 1
        else:
            gen_wu_xing[ben_ming_wu_xing] = 1
        gen_wu_xing[ben_ming_wu_xing[-1]] = ben_ming_wu_xing
        wu_x_lack = []
        for w in wu_xing:
            if w in gen_wu_xing.keys():
                continue
            else:
                wu_x_lack.append(w)
        return wu_x_lack


# 测试
def ba_zi(ct):
    ln = Lunar(ct)
    print('公历 {}  北京时间 {}'.format(ln.localtime.date(), ln.localtime.time()))
    print('{} {}年'.format(ln.ln_date_str(), ln.sx_year()))
    print('年本命 {}'.format(ln.nian_ben_ming[ln.gz_year()]))
    print('{} {} {} {}'.format(ln.gz_year(), ln.gz_month(), ln.gz_day(), ln.gz_hour()))
    print('{} {} {} {}'.format(ln.gz_to_wu_xing(ln.gz_year()), ln.gz_to_wu_xing(ln.gz_month()), ln.gz_to_wu_xing(ln.gz_day()), ln.gz_to_wu_xing(ln.gz_hour())))
    print('{}'.format(ln.gen_wu_xing()))
    print('五行缺 {}'.format(ln.wu_xing_lack()))
    # print('节气：{}'.format(ln.ln_jie()))


if __name__ == '__main__':
    ct0 = datetime.datetime(2019, 7, 16, 10, 50, 15)
    # ct1 = datetime.datetime(1988, 12, 26, 23, 6, 15)
    # ct2 = datetime.datetime(2019, 3, 2, 19, 6, 15)
    ba_zi(ct0)
    # ba_zi(ct1)
    # ba_zi(ct2)
