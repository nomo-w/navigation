# coding: utf-8


from db.base import DBbase


"""
CREATE TABLE `site_sheng` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `sheng` varchar(200) NOT NULL,
  `need_switch` tinyint(1) DEFAULT 0,
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `is_active` tinyint(1) DEFAULT 1,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
"""


class Sheng(DBbase):
    """路由表"""
    def __init__(self):
        super().__init__()

    def get_sheng(self):
        r = self.execute('select id,sheng,need_switch from site_sheng where is_active=1;', fetch=True)
        return {'id': r[0][0], 'area': r[0][1], 'need_switch': r[0][2]}

    def get_need_switch(self):
        r = self.execute('select sheng from site_sheng where need_switch=1;', fetch=True)
        return [i[0] for i in r] if r else []

    def get_need_switch_id(self):
        r = self.execute('select id from site_sheng where need_switch=1;', fetch=True)
        return [i[0] for i in r] if r else []

    def insert_data(self, sheng):
        self.execute(f'insert into site_sheng (sheng) values ("{sheng}");', commit=True)

