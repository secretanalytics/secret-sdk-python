#!/bin/bash
set -o errexit -o nounset -o pipefail
command -v shellcheck >/dev/null && shellcheck "$0"

echo "install betterproto... pre-release for now. stable one has some issues"
pip install --upgrade "betterproto[compiler]" --pre

OUT_DIR="./secret_proto"

mkdir -p "$OUT_DIR"

echo "Processing secretd proto files ..."

SECRETD_DIR="../../../SecretNetwork-master/proto"
SECRETD_THIRD_PARTY_DIR="../../../SecretNetwork-master/third_party/proto"

protoc \
  --proto_path=${SECRETD_DIR} \
  --proto_path=${SECRETD_THIRD_PARTY_DIR} \
  --python_betterproto_out="${OUT_DIR}" \
  $(find ${SECRETD_DIR} ${SECRETD_THIRD_PARTY_DIR} -path -prune -o -name '*.proto' -print0 | xargs -0)
