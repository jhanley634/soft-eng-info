
# stuck postgres lock

![stuck in a lock](asset/2021-12-19/first-lock.jpg)

Relational databases are great, they offer ACID promises:

- atomic
- consistent (e.g. with [MVCC](https://en.wikipedia.org/wiki/Multiversion_concurrency_control))
- isolated
- durable

However, to make good on these promises we often need to
acquire various locks, and occasionally things don't quite work out.
If postgres detects deadlock it will choose a victim process
and the diagnostic is pretty clear.
But sometimes it just hangs endlessly.
An easy way to provoke such behavior is for a DBA to pick
a relation that a busy web server keeps hitting,
and issue ALTER TABLE on it.
The DBA's Exclusive mode lock will be starved out by all those reader locks.

Use a query like this to diagnose:

    SELECT locktype, database, relation, c.relname, c.reltuples, transactionid, pid, mode, granted
    FROM pg_locks
    JOIN pg_class c ON relation = c.oid
    WHERE mode != 'AccessShareLock' AND fastpath = 'f'
    ;

Given a `pid` or two of interest ( e.g. `1234`), investigate details with a query like:

    SELECT pid, datid, datname, usename, client_addr, client_port, xact_start, state, query
    FROM pg_stat_activity
    WHERE state != 'idle' AND pid IN (1234)
    ;

To politely ask a long-running JOIN query to stop, use:

        SELECT pg_cancel_backend(1234);

To more aggressively send a SIGTERM signal to it, use:

        SELECT pg_terminate_backend(1234);

## mysql

With MariaDB / mysql, these commands can shed light on similar lock issues:

        mysql> show open tables  from my_db  where Name_locked > 0;

        mysql> show full processlist;

        mysql> show engine innodb status \G
