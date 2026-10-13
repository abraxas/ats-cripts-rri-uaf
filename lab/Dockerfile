# G8 lab layer on the shared ATS 10.2.0 image. Adds the cripts compiler.
FROM ats-10.2.0-lab:local

USER root
ENV ATS_ROOT=/opt/ats \
    PATH="/opt/ats/bin:${PATH}" \
    LD_LIBRARY_PATH="/opt/ats/lib" \
    CACHE_DIR=/tmp/ats-cache

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        bash \
        g++ \
        libfmt-dev \
        libpcre2-dev \
        libssl-dev \
    && rm -rf /var/lib/apt/lists/*

COPY cripts-compiler.sh /opt/ats/libexec/cripts-compiler.sh
COPY compiler-wrap.sh /opt/ats/bin/compiler.sh
COPY ts-random-stub.cc /tmp/ts-random-stub.cc
RUN g++ -shared -fPIC -o /opt/ats/lib/libtsrandomstub.so /tmp/ts-random-stub.cc \
    && chmod 0755 /opt/ats/bin/compiler.sh /opt/ats/libexec/cripts-compiler.sh \
    && printf '/opt/ats/lib\n' >/etc/ld.so.conf.d/ats.conf \
    && ldconfig \
    && mkdir -p /opt/ats/var/trafficserver /opt/ats/var/log/trafficserver /tmp/ats-cache \
    && chmod 1777 /tmp/ats-cache \
    && test -f /opt/ats/lib/libcripts.so \
    && test -f /opt/ats/lib/libtsrandomstub.so \
    && test -f /opt/ats/include/cripts/Preamble.hpp

WORKDIR /opt/ats
EXPOSE 8080
CMD ["traffic_server"]
