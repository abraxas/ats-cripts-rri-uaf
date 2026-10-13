#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export COMPOSE_PROJECT_NAME="${COMPOSE_PROJECT_NAME:-ats-cripts-rri-uaf}"
export PYTHONUNBUFFERED=1

LABEL="ats-cripts-rri-uaf"
WITNESS="ATS-CRIPTS-RRI-UAF-WITNESS"
IMAGE="ats-10.2.0-lab:local"
LOCK="/tmp/ats-10.2.0-lab.lock"
PIN="b1df7334b39a878971c376da849e8da4984918b6"
ATS_SRC="$(cd ../../client-reviews/trafficserver/src && pwd)"

down() {
  echo "== docker compose down -v =="
  docker compose -p "${COMPOSE_PROJECT_NAME}" down -v --remove-orphans || true
}

fail_setup() {
  local reason="$1"
  echo "FAIL ${LABEL} ${reason} ${WITNESS}" | tee poc-last-run.txt
  down
  exit 1
}

echo "== pin check =="
if [[ ! -f "${ATS_SRC}/CMakeLists.txt" ]]; then
  fail_setup "ats-src-missing"
fi
head_sha="$(git -C "${ATS_SRC}" rev-parse HEAD 2>/dev/null || true)"
if [[ -n "${head_sha}" && "${head_sha}" != "${PIN}" ]]; then
  echo "WARN ats-src-sha=${head_sha} expected=${PIN}"
fi

echo "== docker compose down (clean) =="
down

echo "== shared image ${IMAGE} (lock ${LOCK}) =="
set +e
python3 - "${LOCK}" "${IMAGE}" "${PWD}/Dockerfile.ats-lab" "${PWD}/ats.dockerignore" "${ATS_SRC}" <<'PY'
import fcntl
import os
import subprocess
import sys

lock_path, image, dockerfile, ignorefile, src = sys.argv[1:]
os.makedirs(os.path.dirname(lock_path) or ".", exist_ok=True)


def has_cripts() -> bool:
    inspect = subprocess.run(
        ["docker", "image", "inspect", image],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    if inspect.returncode != 0:
        return False
    probe = subprocess.run(
        [
            "docker",
            "run",
            "--rm",
            "--user",
            "0",
            "--entrypoint",
            "test",
            image,
            "-f",
            "/opt/ats/lib/libcripts.so",
        ],
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return probe.returncode == 0


with open(lock_path, "a+", encoding="utf-8") as lockf:
    fcntl.flock(lockf.fileno(), fcntl.LOCK_EX)
    if has_cripts():
        print(f"shared-image-present {image} cripts=yes", flush=True)
        raise SystemExit(0)
    print(f"== docker build {image} ENABLE_CRIPTS=ON ==", flush=True)
    cmd = ["docker", "build", "-t", image, "-f", dockerfile]
    help_txt = subprocess.run(
        ["docker", "build", "--help"],
        check=False,
        capture_output=True,
        text=True,
    )
    if "--ignorefile" in (help_txt.stdout + help_txt.stderr):
        cmd.extend(["--ignorefile", ignorefile])
    cmd.append(src)
    raise SystemExit(subprocess.call(cmd))
PY
image_rc=$?
set -e
if [[ "${image_rc}" -ne 0 ]]; then
  fail_setup "ats-image-build-failed"
fi

if ! docker image inspect python:3.12-alpine >/dev/null 2>&1; then
  echo "== docker pull python:3.12-alpine =="
  docker pull python:3.12-alpine || fail_setup "origin-image-pull-failed"
fi

echo "== docker compose up --build =="
up_ok=0
for attempt in $(seq 1 8); do
  if docker compose -p "${COMPOSE_PROJECT_NAME}" up --build -d; then
    up_ok=1
    break
  fi
  echo "compose-up-retry attempt=${attempt}"
  sleep 10
  down
done
if [[ "${up_ok}" != 1 ]]; then
  fail_setup "compose-up-failed"
fi

echo "== wait traffic_server 127.0.0.1:18780 health =="
ok=0
for i in $(seq 1 90); do
  if python3 - <<'PY' 2>/dev/null
from http.client import HTTPConnection

conn = HTTPConnection("127.0.0.1", 18780, timeout=3)
conn.request("GET", "/", headers={"Host": "ats-health", "Connection": "close"})
resp = conn.getresponse()
status = resp.status
resp.read()
conn.close()
raise SystemExit(0 if status == 200 else 1)
PY
  then
    ok=1
    echo "health-ready attempt=${i}"
    break
  fi
  echo "health-wait attempt=${i}"
  sleep 2
done
if [[ "${ok}" != 1 ]]; then
  echo "== compose logs (not ready) =="
  docker compose -p "${COMPOSE_PROJECT_NAME}" logs --no-color --tail=120 || true
  fail_setup "ats-port-not-ready"
fi

echo "== poc.py =="
set +e
python3 ./poc.py | tee poc-last-run.txt
rc=${PIPESTATUS[0]}
set -e

if ! tail -n1 poc-last-run.txt 2>/dev/null | grep -qE '^(SUCCESS|FAIL) '; then
  echo "FAIL ${LABEL} poc-exit=${rc} ${WITNESS}" >> poc-last-run.txt
  rc=1
fi

down
exit "${rc}"
