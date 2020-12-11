# coding: utf-8


from db.base import DBbase


"""
CREATE TABLE `site_peizhi` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `need_display_main` tinyint(1) DEFAULT 0,
  `need_display_logo` tinyint(1) DEFAULT 0,
  `need_switch` tinyint(1) DEFAULT 0,
  `switch_time_start` varchar(200) NOT NULL,
  `switch_time_end` varchar(200) NOT NULL,
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
"""


class PeiZhi(DBbase):
    """路由表"""
    def __init__(self):
        super().__init__()

    def get_peizhi(self):
        r = self.execute('select need_display_main,need_display_logo,need_switch,switch_time_start,switch_time_end from site_peizhi;', fetch=True)
        return {'a': r[0][0], 'b': r[0][1], 'need_switch': r[0][2], 'switch_time_start': r[0][3], 'switch_time_end': r[0][4]} \
            if r else {'a': 0, 'b': 0, 'need_switch': 0, 'switch_time_start': '', 'switch_time_end': ''}

    def get_simple(self):
        r = self.execute('select need_display_main,need_display_logo from site_peizhi;', fetch=True)
        return {'a': r[0][0], 'b': r[0][1]}

    def update_peizhi(self, domains, need_display_main, need_display_logo, need_switch, switch_area=[], switch_time_start='', switch_time_end=''):
        sql = f'update site_peizhi set need_display_main={need_display_main},need_display_logo={need_display_logo},' \
              f'need_switch={need_switch},switch_time_start="{switch_time_start}",switch_time_end="{switch_time_end}";'
        self.execute('update site_sheng set need_switch=0;')
        for i in switch_area:
            if i:
                self.execute(f'update site_sheng set need_switch=1 where id={i};')
        self.execute(f'delete from site_main_domain;')
        for i in domains:
            if i:
                self.execute(f'insert into site_main_domain (domain) values ("{i}");')
        return self.execute(sql, commit=True)

