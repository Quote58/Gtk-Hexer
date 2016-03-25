main:	_rom_functions.so rom_functions.py
	cp _rom_functions.so /home/michael/GTK/Hexer/_rom_functions.so
	cp rom_functions.py /home/michael/GTK/Hexer/rom_functions.py

_rom_functions.so:	rom_functions.o rom_functions_wrap.o
	ld -shared rom_functions.o rom_functions_wrap.o -o _rom_functions.so

rom_functions.o:	rom_functions.c
	gcc -fpic -c rom_functions.c -I/usr/include/python3.5m

rom_functions_wrap.o:	rom_functions_wrap.c
	gcc -fpic -c rom_functions_wrap.c -I/usr/include/python3.5m

rom_functions_wrap.c:	rom_functions.i
	swig -python rom_functions.i

rom_functions.py:	rom_functions.i
	swig -python rom_functions.i

clean:
	rm -f rom_functions.o rom_functions_wrap.o rom_functions.py _rom_functions.so
