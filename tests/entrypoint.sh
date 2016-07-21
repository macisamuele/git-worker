#!/bin/bash
go run support/fake-auth-backend.go ~+/test/data/test.git &
./gitlab-git-http-server -listenAddr 0.0.0.0:8181
