#!/bin/bash

BACKUP_PATH=/data/backup/mysql
CURRENT_TIME=$(date +%Y%m%d_%H%M%S)

[ ! -d "$BACKUP_PATH" ] && mkdir -p "$BACKUP_PATH"

#数据库地址
HOST=localhost
#数据库用户名
DB_USER=root
#数据库密码
DB_PW=password

# 要备份的数据库名
DATABASE=blog
FILE_GZ=${BACKUP_PATH}/$CURRENT_TIME.$DATABASE.sql.gz
/usr/local/bin/mysqldump -u${DB_USER} -p${DB_PW} --host=$HOST -q -R --databases $DATABASE  | gzip > $FILE_GZ # 此处必须要用绝对路径

# 所有数据库
#mysqldump --all-databases -xxxxx

# 使用 mutt 发送邮件
echo "数据库备份--$FILE_GZ" | mutt -s "$DATABASE备份" xxx@163.com -a $FILE_GZ

# 删除 7 天以前的备份 「注意写法」
cd $BACKUP_PATH
find $BACKUP_PATH -mtime +7 -name "*sql.gz"  -exec rm -f {} \;
