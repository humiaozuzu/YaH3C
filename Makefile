prefix= /home/${SUDO_USER}/.yah3c

all:
	python setup.py build

install:
	if [ -f ${prefix} ]; then rm -f ${prefix} && mkdir ${prefix} ; fi
	python setup.py install 
	cp -r ./yah3c/plugins ${prefix}
	chown ${SUDO_USER} -R ${prefix}
