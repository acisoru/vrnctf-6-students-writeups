FROM alpine:3.19 as base

FROM base as builder
RUN mkdir /app
WORKDIR /app
RUN apk add --no-cache tzdata go
COPY . .
RUN go mod download
RUN go build -o replicant .

## UNCOMMENT IF NOT USING ENOVY SIDECAR
FROM base as intermediate
WORKDIR /tmp
RUN apk add wget unzip
RUN wget https://github.com/improbable-eng/grpc-web/releases/download/v0.15.0/grpcwebproxy-v0.15.0-linux-x86_64.zip
RUN unzip grpcwebproxy-v0.15.0-linux-x86_64.zip

FROM base as runner
RUN apk add --no-cache tzdata
RUN mkdir /app
COPY --from=builder /app/replicant /app
COPY --from=intermediate /tmp/dist/grpcwebproxy-v0.15.0-linux-x86_64 /app
RUN chmod +x /app/*

RUN echo 'vrnctf{G4RB4G3_RPC_Y0U_SEE}' > /app/flag.txt

EXPOSE 8080

CMD ["/bin/sh", "-c", "nohup sh -c '/app/replicant &' && /app/grpcwebproxy-v0.15.0-linux-x86_64 --backend_addr=localhost:8070 --run_tls_server=false --allow_all_origins"]
#CMD ["/app/replicant"]