all: start_service

cli_shortcuts:
	cp ./cli_shortcuts/* ~/
	source ~/.aws-a
	chmod go-rwx cluster
	chmod go-rwx cluster/*
	

start_service:
	make -f eks.mak start

