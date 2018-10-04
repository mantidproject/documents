The following table majorly lists the remote machines (Host) by their name and installed MantidPlot versions (Stable and eventually Unstable).

| Host       | Stable | Nightly            | Unstable           | Location | Ubuntu         |
|------------|--------|--------------------|--------------------|----------|----------------|
| mantidtest | 3.12.1 |                    |                    | CS-lab   | 16.04.4 LTS    |
| in4lnx     | 3.13   | 3.13.20180913.1120 | 3.12.20180329.907  |          | 16.04.4 LTS    |
| in5lnx     | 3.13   | 3.13.20180913.1120 | 3.11.20180302.638  |          | 16.04.4 LTS    |
| in6lnx     | 3.13   | 3.13.20180913.1120 | 3.11.20180302.638  |          | 16.04.1 LTS    |  
| in16blnx   | 3.13   |                    |                    |          | 16.04.4 LTS    |
| d17lnx     | 3.13   |                    | 3.11.20180315.1345 |          | 16.04.4 LTS    |
| figarolnx  | 3.13   |                    |                    |          | 16.04.1 LTS    |
| d2blnx     | 3.13   |                    | 3.12.20180425.839  |          | 16.04.1 LTS    |
| d20lnx     | 3.12.0 |                    | 3.12.20180418.2323 |          | 16.04.4 LTS    |
| d11lnx     | 3.13   |                    |                    |          |                |

**Updating the machines**

There is a special user `mantid` which should be used to perform the updates. To switch users,

```
su mantid
```

To get to `mantid`'s home directory,

```
cd
```

Subdirectory `remotes` in `mantid`'s home contains the scripts needed to update Mantid (release and nightly).

The master script `update.sh` runs the show. To update the official releases,

```
./update.sh mantid.sh
```

To update the nightlies,

```
./update.sh mantidnightly.sh
```

`update.sh` connects to each remote server running the argument script there. The machines are listed in `update.sh` so when new machines are added the script need to be updated.

The files `mantid.sh.done` and `mantidnightly.sh.done` contain a list of servers where the last update was succesfull. It is a good idea to remove these files before performing an update.

The `update.sh` script will check if a remote is accessible by `ping`. It also checks if `MantidPlot` is already running on a machine. If so, the remote is be skipped.

A list of successful updates and failures will be printed after `update.sh` finishes. Observe the list carefully!
