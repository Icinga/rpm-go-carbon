#!/bin/bash

set -ex

: ${VERSION:='0.11.0'}
: ${BRANCH:="v${VERSION}"}
: ${WORKDIR:="go-carbon"}

if [ ! -d "$WORKDIR" ]; then
    git clone --depth=1 --recursive \
        https://github.com/lomik/go-carbon -b "${BRANCH}" "$WORKDIR"
    cd "$WORKDIR"
else
    cd "$WORKDIR"
    git fetch origin
    git checkout --force "$BRANCH"
    git submodule sync
    git submodule update --init
fi

../git-archive-all --prefix "go-carbon-${VERSION}/" "../go-carbon-${VERSION}-bundled.tar.gz"
