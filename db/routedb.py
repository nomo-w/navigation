# coding: utf-8


from db.base import DBbase


"""
CREATE TABLE `site_route` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `route` varchar(200) NOT NULL,
  `jumpto` varchar(200) NOT NULL,
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `is_active` tinyint(1) DEFAULT 1,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
"""


class Route(DBbase):
    """路由表"""
    def __init__(self):
        super().__init__()

    def get_route(self, site):
        r = self.execute(f'select jumpto from site_route where route="{site}" and is_active=1;', fetch=True)
        return r[0][0] if r else None

    def insert_data(self, route, jumpto):
        return self.execute(f'insert into site_route (route,jumpto) values ("{route}","{jumpto}");', commit=True)

