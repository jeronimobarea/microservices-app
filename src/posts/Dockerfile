FROM golang:1.13

WORKDIR /server/src/posts
COPY . .

RUN go get -d -v ./...
RUN go install -v ./...

CMD ["go run *.go"]