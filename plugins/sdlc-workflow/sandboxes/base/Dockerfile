FROM registry.access.redhat.com/ubi10/ubi:latest

ARG NODE_MAJOR=22
ARG GH_CLI_VERSION=2.74.1
ARG CLAUDE_CODE_VERSION=latest

RUN dnf install -y \
      git \
      openssh-clients \
      python3 \
      curl \
      jq \
      tar \
      gzip \
      findutils \
      procps-ng \
    && dnf clean all

RUN curl -fsSL https://rpm.nodesource.com/setup_${NODE_MAJOR}.x | bash - \
    && dnf install -y nodejs \
    && dnf clean all

RUN ARCH=$(uname -m) \
    && if [ "$ARCH" = "x86_64" ]; then GH_ARCH="linux_amd64"; \
       elif [ "$ARCH" = "aarch64" ]; then GH_ARCH="linux_arm64"; \
       else echo "Unsupported architecture: $ARCH" && exit 1; fi \
    && curl -fsSL "https://github.com/cli/cli/releases/download/v${GH_CLI_VERSION}/gh_${GH_CLI_VERSION}_${GH_ARCH}.tar.gz" \
       | tar -xz --strip-components=1 -C /usr/local

RUN if [ "$CLAUDE_CODE_VERSION" = "latest" ]; then \
      npm install -g @anthropic-ai/claude-code; \
    else \
      npm install -g "@anthropic-ai/claude-code@${CLAUDE_CODE_VERSION}"; \
    fi

RUN groupadd -r sandbox \
    && useradd -r -g sandbox -m -d /home/sandbox -s /bin/bash sandbox

COPY plugins/sdlc-workflow/ /home/sandbox/.claude/plugins/sdlc-workflow/

RUN chown -R sandbox:sandbox /home/sandbox

USER sandbox
WORKDIR /home/sandbox

CMD ["/bin/bash"]
