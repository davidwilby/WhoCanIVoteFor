#!/usr/bin/env bash
set -xeE

# EE
sudo cat > /etc/cron.d/every_election_cron <<- EOF
0 3 * * * ee-manage-py-command sync_elections
EOF