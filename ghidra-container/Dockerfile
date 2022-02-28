FROM gradle:7.4-jdk11

ENV GHIDRA_SHA256 ac96fbdde7f754e0eb9ed51db020e77208cdb12cf58c08657a2ab87cb2694940
ENV GHIDRA_URL https://github.com/NationalSecurityAgency/ghidra/releases/download/Ghidra_10.1.2_build/ghidra_10.1.2_PUBLIC_20220125.zip

RUN apt-get update -y && \
    apt-get install -y libxtst6 libxi6 libxrender1 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN useradd -m -u 1001 noroot
USER noroot
WORKDIR /home/noroot

# Download, check the checksum, and unzip Ghidra. Then we clean up.
RUN curl -L "${GHIDRA_URL}" > /tmp/ghidra.zip && \
    echo "${GHIDRA_SHA256} /tmp/ghidra.zip" | sha256sum -c - && \
    unzip /tmp/ghidra.zip && \
    mv ghidra_10.1.2_PUBLIC ~/ghidra && \
    chmod +x ~/ghidra/ghidraRun
