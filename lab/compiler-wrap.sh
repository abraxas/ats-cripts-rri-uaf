#!/bin/bash
set -euo pipefail
: "${ATS_ROOT:=/opt/ats}"
: "${CXX:=g++}"
export ATS_ROOT CXX
export CACHE_DIR="${CACHE_DIR:-/tmp/ats-cache}"
mkdir -p "${CACHE_DIR}"
flags="-x c++ -std=c++20 -I${ATS_ROOT}/include -L${ATS_ROOT}/lib"
flags="${flags} -Wl,-rpath,${ATS_ROOT}/lib -fPIC"
if ldd "${ATS_ROOT}/bin/traffic_server" 2>/dev/null | grep -q libasan; then
  flags="${flags} -fsanitize=address -fno-omit-frame-pointer"
fi
export CXXFLAGS="${CXXFLAGS:-${flags}}"
exec /bin/bash /opt/ats/libexec/cripts-compiler.sh "$@"
