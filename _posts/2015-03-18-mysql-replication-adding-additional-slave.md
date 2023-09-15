---
layout: post
title: "MySQL replication – adding additional slave"
author: Jakob Aarøe Dam
---

*Master-slave replication is a common means to increase SQL
performance. This post describes how to add an additional slave
running on Ubuntu 14.04 Server. Replication of the master database
(4.5G) is initially performed with mysqldump, and replication is
started afterwards.*

The scenario is a web-server setup where the capacity of the existing
master-slave setup is maxed out. We'll add an extra slave to take some
of the load; especially gaining extra SQL read capacity. The existing
setup runs on stale Ubuntu 11.10 virtual machines – we'll take the
plunge and add the new slave on Ubuntu 14.04 (LTS) in the same go.

Setup:
<table>
	<tr>
    	<th width="70px">Role</th><th>Before</th><th>After</th>
    </tr>
    <tr>
    	<td>Master</td>
    	<td>Ubuntu 11.10, MySQL 5.1.69</td>
        <td>Ubuntu 11.10, MySQL 5.1.69</td>
    </tr>
    <tr>
    	<td>Slave 1</td>
        <td>Ubuntu 11.10, MySQL 5.1.69</td>
        <td>Ubuntu 11.10, MySQL 5.1.69</td>
    </tr>
    <tr>
    	<td>Slave 2</td>
        <td></td>
        <td>Ubuntu 14.04, MySQL 5.5.40</td>
    </tr>
</table>

## Preparation

The new Ubuntu 14.04 server is setup with an OS disk and a data disk
for easier future maintenance. The disk layout looks as follows: 

```bash
slave: $ lsblk | grep vd  
vda    253:0    0    20G  0 disk  
├─vda1 253:1    0  19.5G  0 part /
├─vda2 253:2    0     1K  0 part 
└─vda5 253:5    0   510M  0 part [SWAP]
vdb    253:16   0    20G  0 disk  
└─vdb1 253:17   0    20G  0 part /var/www
```

MySQL databases are moved to the data disk in `/var/www/mysql` instead
of the standard location in `/var/lib/mysql` – which is replaced with
a symbolic link, minimizing the confusion of sysadmins accessing the
server later on.

```bash
slave: $ mv /usr/lib/mysql /var/www/mysql
slave: $ ln -s /var/www/mysql /usr/lib/mysql 
```

A common gotcha with placing the databases outside the common location
is that [AppArmor](https://en.wikipedia.org/wiki/AppArmor) restricts
MySQL access outside a predefined list of locations. MySQL is allowed
access by adding relevant paths to the AppArmor profile for MySQL:

```bash
slave: $ cat >> /etc/apparmor.d/local/usr.sbin.mysqld <<EOF
/var/www/mysql/ r,
/var/www/mysql/** rwk,
EOF
slave: $ service apparmor reload
```

In the replication master-slave setup servers identify themselves
using the `server-id` property (a positive integer setup in the MySQL
configuration). When the slave starts it opens a connection to the
master which streams changes into the relay log. Unless the
`relay-log` and `relay-log-index` are explicitly named in the
configuration, the standard naming includes the hostname, which
results in a number of problems
(http://dev.mysql.com/doc/refman/5.7/en/slave-logs-relaylog.html)

In our setup, the existing master contains several databases but, only
one is relevant for the new slave, namely the database named `db`;
this is reflected in the configuration parameter `replicate-do-db`
below. Note, however, that changes, to the master, is still sent and
written to the slave in a relay log file.

The changes to the MySQL standard configuration are added:

```bash
slave: $ cat > /etc/mysql/conf.d/slave.cnf <<EOF
[mysqld]
server-id               = 4
relay-log               = mysql-relay-bin.log
relay-log-index         = mysql-relay-bin.index
replicate-do-db         = db
```

Create the database and add a user. As an additional pre-caution the
user is restricted to read-only access, since the slave should never
be written to directly:

```bash
slave: $ mysql -u root -p
mysql> CREATE DATABASE db;
mysql> GRANT select ON db.* to 'user'@'localhost' identified by 'password';
```

Load relevant timezone information into MySQL:

```bash
slave: $ mysql_tzinfo_to_sql /usr/share/zoneinfo/Europe/Copenhagen 'Europe/Copenhagen' | mysql -u root --password=$DB_PWD mysql
```

## Dump master database

The MySQL manual, describes how to setup an additional slave by
replicating another slave:
[replication-howto-additionalslaves](http://dev.mysql.com/doc/refman/5.5/en/replication-howto-additionalslaves.html). The
approach shuts down the slave database, while copying the data.

Another approach is to `mysqldump` or `rsync` the database from the
master database, locking it for writes beforehand. This keeps the
database slaves running, which in our setup is less obtrusive. Since
we are crossing MySQL versions – 5.1 -> 5.5 – we'll use `mysqldump` to
extract the data (I did not try `rsync` though).

On master:

```bash
master: $ mysql -u root -p
mysql> use db;
mysql> FLUSH TABLES WITH READ LOCK;
mysql> SHOW MASTER STATUS;
+------------------+----------+--------------+..
| File             | Position | Binlog_Do_DB | 
+------------------+----------+---------------..
| mysql-bin.004488 | 11131082 | db           |
+------------------+----------+--------------+..
-- do mysqldump in another session
mysql> UNLOCK TABLES;
mysql> QUIT;
```

In another SSH session on master:

```bash
master: $ mysqldump -u root -p db > db.sql
```

## Load database and initialize slave

After moving the database dump to the slave load it:

```bash
slave: $ mysql -u root -p db < db.sql
```

Load the slave with connection and replication information about the
master, and start it:

```bash
mysql> CHANGE MASTER TO
  MASTER_HOST='10.2.10.2',
  MASTER_USER='repl',
  MASTER_PASSWORD='repl-password', 
  MASTER_LOG_FILE='mysql-bin.004488', 
  MASTER_LOG_POS=11131082;
mysql> START SLAVE;
```

If the slave has access to the master database, relay files should now
start to stream to the slave.

## Debugging

Check the slave status to ensure things are working as expected:

```bash
slave: $ mysql -u root -p
mysql> show slave status\G;
*************************** 1. row ***************************
               Slave_IO_State: Waiting for master to send event
                  Master_Host: 10.2.10.2
                  Master_User: repl
                  Master_Port: 3306
                Connect_Retry: 60
              Master_Log_File: mysql-bin.004536
          Read_Master_Log_Pos: 69346276
               Relay_Log_File: mysql-relay-bin.000146
                Relay_Log_Pos: 69122883
        Relay_Master_Log_File: mysql-bin.004536
             Slave_IO_Running: Yes
            Slave_SQL_Running: Yes
              Replicate_Do_DB: db
...
```

Check the status of the MySQL I/O and SQL threads:

```bash
mysql> show processlist;
+------+-------------+-----------+------+---------+--------+----------------------------------+
| Id   | User        | Host      | db   | Command | Time   | State                            |
+------+-------------+-----------+------+---------+--------+----------------------------------+
|    1 | system user |           | NULL | Connect |      8 | Slave has read all relay log     |
|    2 | system user |           | NULL | Connect | 552110 | Waiting for master to send event |
| 2264 | root        | localhost | NULL | Sleep   |  19896 |                                  |
| 2334 | root        | localhost | NULL | Query   |      0 | NULL                             |
+------+-------------+-----------+------+---------+--------+----------------------------------+
4 rows in set (0.00 sec)
```

## Conclusion

I can confirm that things are working smoothly with this setup. The
next step is to upgrade the two stale Ubuntu 11.10 database servers.

