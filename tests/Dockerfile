FROM golang:1.6.3

# Guide on https://gitlab.com/gitlab-org/gitlab-git-http-server
RUN cd / && \
    git clone https://gitlab.com/gitlab-org/gitlab-git-http-server.git && \
    cd gitlab-git-http-server && \
    make && \
    wget -O /usr/local/bin/dumb-init https://github.com/Yelp/dumb-init/releases/download/v1.1.1/dumb-init_1.1.1_amd64 && \
    chmod +x /usr/local/bin/dumb-init 

COPY entrypoint.sh /gitlab-git-http-server/entrypoint.sh
RUN chmod +x /gitlab-git-http-server/entrypoint.sh && ./endpoint &

COPY generate_repositories.sh /gitlab-git-http-server/generate_repositories.sh
RUN bash /gitlab-git-http-server/generate_repositories.sh


EXPOSE 8181

WORKDIR /gitlab-git-http-server
CMD [ "dumb-init", "./entrypoint.sh" ]

