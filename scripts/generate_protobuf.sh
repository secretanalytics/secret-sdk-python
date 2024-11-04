#!/bin/bash
set -o errexit -o nounset -o pipefail

SCRIPT_PATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

rm -rf "${SCRIPT_PATH}/SecretNetwork"
git clone --depth 1 --branch v1.15.0-beta.0 https://github.com/scrtlabs/SecretNetwork "${SCRIPT_PATH}/SecretNetwork"

SECRET_DIR="${SCRIPT_PATH}/SecretNetwork/proto"
SECRET_THIRD_PARTY_DIR="${SCRIPT_PATH}/SecretNetwork/third_party/proto"

#!/bin/bash
set -o errexit -o nounset -o pipefail
command -v shellcheck >/dev/null && shellcheck "$0"

OUT_DIR="../secret_sdk/protobuf/"

mkdir -p "$OUT_DIR"

echo "Processing secret proto files ..."

protoc \
  --proto_path=${SECRET_DIR} \
  --proto_path=${SECRET_THIRD_PARTY_DIR} \
  --python_betterproto_out="${OUT_DIR}" \
  $(find ${SECRET_DIR} ${SECRET_THIRD_PARTY_DIR} -path -prune -o -name '*.proto' -print0 | xargs -0)