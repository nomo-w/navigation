# coding: utf-8


from db.base import DBbase


"""
CREATE TABLE `site_main_domain` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `domain` varchar(200) NOT NULL,
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `is_active` tinyint(1) DEFAULT 1,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
"""


class MainDomain(DBbase):
    """路由表"""
    def __init__(self):
        super().__init__()

    def get_domain(self):
        r = self.execute('select domain from site_main_domain where is_active=1;', fetch=True)
        return [i[0] for i in r] if r else []
