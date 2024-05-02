FROM ubuntu:22.04@sha256:b492494d8e0113c4ad3fe4528a4b5ff89faa5331f7d52c5c138196f69ce176a6 as builder

RUN apt update && apt install -y gcc

WORKDIR build/

COPY ./main.c .

RUN gcc -pthread -o chall main.c

FROM ubuntu:22.04@sha256:b492494d8e0113c4ad3fe4528a4b5ff89faa5331f7d52c5c138196f69ce176a6

RUN apt update && apt install -y socat

COPY --from=builder /build/chall /app/chall
COPY flag /app

RUN echo "nobody:x:1337:1337:::" > /etc/passwd
RUN echo "nobody::1337:nobody" > /etc/group

WORKDIR /app
USER nobody

CMD ["socat", "TCP-LISTEN:13577,reuseaddr,fork", "EXEC:/app/chall"]