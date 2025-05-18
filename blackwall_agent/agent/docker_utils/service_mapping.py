ports = {
    "ssh": {
        "host_port": 2222,
        "container_port": 2222,
        "proto": "tcp"
    },
    "ftp": {
        "host_port": 2121,
        "container_port": 2121,
        "proto": "tcp"
    },
    "telnet": {
        "host_port": 2323,
        "container_port": 2323,
        "proto": "udp" # or UDP, gonna check it later
    },
    "mysql": {
        "host_port": 3306,
        "container_port": 3306,
        "proto": "tcp"
    },
    "web": {
        "host_port": 80,
        "container_port": 8080, # or 5000, maybe I will use flask with no gunicorn
        "proto": "tcp"
    }
}