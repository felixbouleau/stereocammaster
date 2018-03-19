#!/usr/bin/env bash

## connect to the host's system bus from the application container
export DBUS_SYSTEM_BUS_ADDRESS=unix:path=/host/run/dbus/system_bus_socket

mkdir /img_dir
chmod a+rwg /img_dir

python myserver.py
