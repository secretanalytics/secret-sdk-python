all: init proto-gen format

init:
	@echo "Pull External Protofiles"
	git submodule init
	git submodule update

#@echo "Install dependencies"
#npm i

#format:
#	npm run format

proto-gen: 
	@echo "Generating Protobuf files"
	./scripts/proto-gen.sh

build: 
	npm run build

publish:
	npm publish

.PHONY: all proto-gen format init build publish
