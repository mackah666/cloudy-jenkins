.PHONY: clean prepare build release

OS:=6
BUILD_NUMBER:=$(shell date +%Y%m%d%H%M%S)
SERVICE:=

clean:
	rm -rf SOURCES RPMS SRPMS

prepare:
	mkdir -p SOURCES
	tar --exclude "*.sw?" -czf SOURCES/src.tar.gz src

build: clean prepare
	mock-build --os $(OS) --define "BUILD_NUMBER $(BUILD_NUMBER)"

release: build
	@[ -n "$(SERVICE)" ] || ( echo "Add SERVICE=service-name-goes-here to the make command and try again" >&2; exit 1 )
	cosmos-release service "$(SERVICE)" RPMS/custom-jenkins-master-*.rpm
