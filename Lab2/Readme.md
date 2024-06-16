## usage
#### directly
```bash
python script.py host
```
#### using docker
```bash
docker build -t mtu .
docker run -it --rm mtu host
```

Both IPv4 and IPv6 are supported but docker should be correctly configured for IPv6 usage.
