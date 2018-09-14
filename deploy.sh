#!/bin/bash
set -eu

if [[ $# -ne 1 ]]; then
	echo >&2 "Usage: $0 futaba-config.toml"
	exit 1
fi

repo_dir="$(dirname "$0")"
dest_dir=~futaba/repo

rm -r "$dest_dir"
mkdir -p "$dest_dir"
cp -a "$repo_dir" "$dest_dir"
install -m400 "$1" "$dest_dir/config.toml"
chown -R futaba:futaba "$dest_dir"
echo "Installed source code to '$dest_dir'"

python3.6 -m pip install -r "$repo_dir/requirements.txt" > /dev/null
echo "Installed Python dependencies"

install -m644 "$repo_dir/misc/futaba.service" /usr/local/lib/systemd/system/futaba.service
chown root:root /usr/local/lib/systemd/system/futaba.service
echo "Installed systemd service"

systemctl daemon-reload
systemctl restart futaba.service
echo "Started futaba systemd service"