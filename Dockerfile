app = "goodlife-gateway-fabric"
primary_region = "syd"

[build]
  dockerfile = "Dockerfile"

[env]
  PYTHONPATH = "/opt/odynex-axis-matrix"
  PYTHONUNBUFFERED = "1"
  DEBIAN_FRONTEND = "noninteractive"

[http_service]
  internal_port = 8080
  force_https = true
  auto_stop_machines = "stop"
  auto_start_machines = true
  min_machines_running = 0
  processes = ["app"]

[[vm]]
  memory = "1gb"
  cpu_kind = "shared"
  cpus = 1
