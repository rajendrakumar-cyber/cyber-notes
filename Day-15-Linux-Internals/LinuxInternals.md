Day 15 – Linux Internals Practice

Today I studied important Linux internal concepts including processes, inodes, IDs, pipes, logs, and runlevels.

1>>Linux Processes

A process is a running program in Linux.

Commands practiced:

ps
ps aux
top
htop
kill PID
kill -9 PID

I learned:

   Every running program has a PID (Process ID).

  The system manages multiple processes at the same time.

  kill is used to terminate processes.

  -9 forcefully stops a process.

Understanding processes is important for system monitoring and troubleshooting.

2>>Process ID (PID) and User ID (UID)

Commands:

id
whoami

I learned:

  PID identifies a running process.

  UID identifies a user.

  Root user has UID 0.

System security depends on user privileges.

3>>Inodes

Inodes store metadata about files, not the file name.

Command:

ls -i

I learned:

  Every file has a unique inode number.

  Hard links share the same inode.

  Inodes store file size, permissions, owner, and timestamps.

  Inodes help understand file structure at a deeper level.
 
4>>Pipes

Pipes send output of one command into another command.

Example:

ls -l | grep txt

I learned:

  The | symbol connects commands.

  Pipes are very powerful for filtering and searching.

  Used heavily in log analysis.

5>>Logs

Important Linux logs:

/var/log/syslog
/var/log/auth.log

Commands:

cat /var/log/auth.log
tail -n 20 /var/log/auth.log

I learned:

  Logs record system activity.

  Authentication logs show login attempts.

  Logs are critical for SOC monitoring.

  Runlevels / System States

Command:

6>>runlevel

Modern systems use systemd, but traditional runlevels include:

0 – Shutdown
1 – Single user mode
3 – Multi-user mode
5 – Graphical mode
6 – Reboot