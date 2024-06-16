import enum
import sys
import subprocess
import platform
import argparse
from rich_argparse import RichHelpFormatter


class PingReport(enum.Enum):
    UNIMPLEMENTED = 5
    ERROR         = 4
    WRONG_HOST    = 3
    FAILURE       = 2
    SUCCESS_IPv6  = 1
    SUCCESS_IPv4  = 0


def ping(host: str, **kwargs) -> PingReport:
    if "IPv6" not in kwargs:
        status = ping(host, IPv6=False, **kwargs)
        if status != PingReport.WRONG_HOST:
            return status
        return ping(host, IPv6=True, **kwargs)
    IPv6 = kwargs["IPv6"]
    size = kwargs["size"] if "size" in kwargs else 0

    system = platform.system()
    if system == "Darwin":
        if not IPv6:
            command = ['ping', '-c', '1', '-t', '2', '-D', '-s', str(max(size - 20 - 8, 0)), host]
            try:
                result = subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except:
                return PingReport.ERROR

            if result.returncode == 68:
                return PingReport.WRONG_HOST
            return PingReport.SUCCESS_IPv4 if result.returncode == 0 else PingReport.FAILURE
        else:
            command = ['ping6', '-c', '1', '-i', '2', '-m', '-m', '-s', str(max(size - 40 - 8, 1)), host]
            try:
                result = subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except:
                return PingReport.ERROR

            if result.returncode == 1:
                return PingReport.WRONG_HOST
            return PingReport.SUCCESS_IPv6 if result.returncode == 0 else PingReport.FAILURE
    elif system == "Linux":
        if not IPv6:
            command = ['ping', '-4', '-c', '1', '-w', '2', '-M', 'do', '-s', str(max(size - 20 - 8, 0)), host]
            try:
                result = subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except:
                return PingReport.ERROR

            if result.returncode == 2:
                return PingReport.WRONG_HOST
            return PingReport.SUCCESS_IPv4 if result.returncode == 0 else PingReport.FAILURE
        else:
            command = ['ping', '-6', '-c', '1', '-w', '2', '-M', 'do', '-s', str(max(size - 40 - 8, 0)), host]
            try:
                result = subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except:
                return PingReport.ERROR

            if result.returncode == 2:
                return PingReport.WRONG_HOST
            return PingReport.SUCCESS_IPv6 if result.returncode == 0 else PingReport.FAILURE
    elif system == "Windows":
        if not IPv6:
            command = ['ping', '-4', '-n', '1', '-w', '2', '-f', '-l', str(max(size - 20 - 8, 0)), host]
            try:
                result = subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except:
                return PingReport.ERROR

            if result.returncode == 2:
                return PingReport.WRONG_HOST
            return PingReport.SUCCESS_IPv4 if result.returncode == 0 else PingReport.FAILURE
        else:
            command = ['ping', '-6', '-n', '1', '-w', '2', '-l', str(max(size - 40 - 8, 0)), host]
            try:
                result = subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except:
                return PingReport.ERROR

            if result.returncode == 2:
                return PingReport.WRONG_HOST
            return PingReport.SUCCESS_IPv6 if result.returncode == 0 else PingReport.FAILURE
    else:
        return PingReport.UNIMPLEMENTED


def find_minimum_mtu(host: str, IPv6: bool, lower_bound: int = 576, upper_bound: int = 10000) -> int:
    print("progress: ", end='', flush=True)
    while lower_bound + 1 < upper_bound:
        mid = (lower_bound + upper_bound) // 2
        if ping(host, IPv6=IPv6, size=mid) in [PingReport.SUCCESS_IPv4, PingReport.SUCCESS_IPv6]:
            lower_bound = mid
        else:
            upper_bound = mid
        print(".", end='', flush=True)
    print()

    return lower_bound


def main() -> int:
    RichHelpFormatter.styles["argparse.groups"] = "green"
    RichHelpFormatter.styles["argparse.prog"] = "default"
    parser = argparse.ArgumentParser(description="Determine the minimum MTU size to a specified IPv4 host.", formatter_class=RichHelpFormatter)
    parser.add_argument('host', type=str, help="IP address or hostname of IPv4 host")
    args = parser.parse_args()

    report = ping(args.host)
    if report == PingReport.UNIMPLEMENTED:
        print(f"Doesn't support your platform {platform.system()}!", file=sys.stderr)
        return 1
    elif report == PingReport.ERROR:
        print("Can't use the ping command!", file=sys.stderr)
        return 2
    elif report == PingReport.WRONG_HOST:
        print(f"Host {args.host} is not valid!", file=sys.stderr)
        return 3
    elif report == PingReport.FAILURE:
        print(f"Host {args.host} is unavailable!", file=sys.stderr)
        return 4

    minimum_mtu = find_minimum_mtu(args.host, IPv6=(report == PingReport.SUCCESS_IPv6))
    print(f"The minimum MTU size to the host {args.host} is {minimum_mtu}.")
    return 0


if __name__ == "__main__":
    exit(main())
