# Lunar
this is a repository for Lunar date convert project
lunar.py
2015/02/27  罗兵  原作者 公历生成农历，年干支、日干支
2019/07/14  张高尉  增加了月干支，时干支，五行分析

1、this is a public project to convert date to lunar date;

2、lunar is very important guid for Chinese farmer in farming.

with this project，it  is convinent for you to get the lunar date and 'gan-zhi' for a date.


following is a example to call this project 
 
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
				

