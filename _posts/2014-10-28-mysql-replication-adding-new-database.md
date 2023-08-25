---
layout: post
title: "MySQL replication – adding new database"
author: Jakob Aarøe Dam
---
    
*A short guide on how to add an additional database in a mysql master-slave setup that uses filtering on the replication*

## Updates to slave

If you filter on the databases to replicate with `replicate-do-db`,
add the new database to the mysql configuration.

```
slave: $ cat >> /etc/mysql/conf.d/slave.cnf <<EOF
replicate-do-db         = db
EOF
```

And restart mysql to load the new configuration:

```
slave: $ service mysql restart
```

## Updates to master

Similarly if the master is also filtering on databases with
`binlog_do_db` the new database should also be added to the master's
configuration.

```
slave: $ cat >> /etc/mysql/conf.d/master.cnf <<EOF
binlog-do-db         = db
EOF
```

And restart the mysql on the master to load the updated configuration:

```
master: $ service mysql restart
```

Now you're ready to go and add the new database to the master, which
if things are working smoothly should replicate to the slave.

```
mysql> create database db;
```

## Debugging

Remember to check that things are working as expected. In the
following case they were not:

~~~ 
mysql> show slave status\G;
*************************** 1. row ***************************
               Slave_IO_State: Waiting for master to send event
                  Master_Host: 10.2.10.2
             Slave_IO_Running: Yes
            Slave_SQL_Running: No
                   Last_Errno: 1007
                   Last_Error: Error 'Can't create database 'db'; database exists' on query...
                 Skip_Counter: 0
~~~

The database already existed on the slave. That makes mysql
replication stop and replication needs manual intervention to start
working again.

Skip past the replication error:

```
mysql> stop slave;
mysql> SET GLOBAL SQL_SLAVE_SKIP_COUNTER = 1;
mysql> start slave;
```

<style>
pre{
	font-size:80%;
}
</style>
