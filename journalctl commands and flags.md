Follow Logs in Real-time: journalctl -f.
journalctl -u nginx.service
Show Recent Logs: journalctl -n 20 (last 20 lines) or journalctl -r (reverse order).
Filter by Priority: journalctl -p err (shows error, critical, alert, and emerg).
View Disk Usage: journalctl --disk-usage.
Clear Logs: sudo journalctl --vacuum-time=2d (keep only last 2 days) or sudo journalctl --vacuum-size=100M
Filter by Time: journalctl --since "1 hour ago" or journalctl --since "2023-10-01 00:00:00" --until "2023-10-02 12:00:00".
journalctl -n 50 (shows the last 50 entries).
journalctl -e
Latest logs for a specific service: journalctl -u service_name -n 20
