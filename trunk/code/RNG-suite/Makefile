TL200: TestU01
	git clone https://github.com/tectrolabs/tl200
	cd tl200 && unzip TL200-kit-2.2-4.zip
	cd tl200 && rm -f TL200-kit-2.3.zip TL200-kit-2.4.zip TL200-kit-2.2-4.zip
	cd tl200/linux-64/getrnd && sudo make

	sudo apt install --reinstall linux-headers-$(uname -r)

	rm tl200/linux-64/tlrandom/tlrandom.c
	cd tl200/linux-64/tlrandom && wget https://raw.githubusercontent.com/mathiashelseth/tl200/master/tlrandom.c -O tlrandom.c
	cd tl200/linux-64/tlrandom && make
	sudo chmod +x tl200/linux-64/tlrandom/ins-tlrandom.sh
	cd tl200/linux-64/tlrandom && sudo ./ins-tlrandom.sh

TestU01: git gcc gpp make tkinter numpy
	git clone https://github.com/umontreal-simul/TestU01-2009.git TestU01
	sudo chmod +x TestU01/configure
	cd TestU01 && ./configure
	cd TestU01 && sudo make
	cd TestU01 && sudo make install

numpy:
	sudo apt-get install python3-numpy

tkinter:
	sudo apt-get install python3-tk

gcc:
	sudo apt-get install gcc

gpp:
	sudo apt-get install g++

git:
	sudo apt-get install git

make:
	sudo apt-get install make

clean:
	rm -rf TestU01
	rm -rf tl200
