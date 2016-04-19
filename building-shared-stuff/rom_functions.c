#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <stdlib.h>

int make_changes(unsigned char *, int, int, size_t, int*);
int get_data(char *, unsigned char **, FILE *, size_t *);
int apply_changes(unsigned char *, char *, size_t);
int not_main(char *, char *, char *, int);

int not_main(char *rom_name, char *offset, char *bytes, int apply_or_check) {

	FILE* file = fopen(rom_name, "rb");
	//printf("trying to open...\n");	

	if (file) {
		size_t size;

		//printf("file exists!\n");
		unsigned char *buf;

		get_data("rom.smc", &buf, file, &size);

		fclose(file);
		//printf("file closed!\n");

		//char input[30];
		char to_use[30];
		//printf("offset?\n");
		//scanf("%s", input);		//needed
		int num = strlen(bytes);	//needed
		
		int offset_to_apply, bytes_to_apply, new_offset;
		int c = 0;
		int check_tweak = 0;

		sscanf(offset, "%x", &offset_to_apply);
		//printf("bytes? (offset is: %d)\n", offset_to_apply);
		//scanf("%s", input);		//needed

		while (c < num) {
			//printf(">>>>>%d<<<<<<\n>>>>>%d<<<<<\n", c, num);
			strncpy(to_use, bytes+c, 2);
			sscanf(to_use, "%x", &bytes_to_apply);

			if ((make_changes(buf, offset_to_apply, bytes_to_apply, size, &check_tweak)==0)) {
				if (apply_or_check == 0) { //0 = apply
					/*switch(apply_changes(buf, rom_name, size)) {
						case 0: printf("success!\n"); break;
						case 1: printf("not success :(\n"); break;
					}*/
					apply_changes(buf, rom_name, size);
				}
			}	
			c += 2;
			offset_to_apply++;
		}
		
		free(buf);

		if (apply_or_check > 0)	//if this is checking stuff
			//printf("number of bytes in the tweak: %d\nnumber of bytes that were the same: %d\n", c/2, check_tweak);
			if (check_tweak == (c/2))
				return 1;
			else
				return 0;

		return 1;
	}

	else {
		fclose(file);
		printf("no such file???\n");
		return 0;
	}
}

int get_data(char *rom, unsigned char **buf, FILE *file, size_t *s) {

	fseek(file,0,SEEK_END);
	*s = ftell(file);

	//printf("%d\n", *s);

	rewind(file);

	//allocate the memory for the rom array
	*buf = malloc(*s);

	//transfer data into array
	fread(*buf, 1, *s, file);

}


int make_changes(unsigned char *buf, int offset_to_apply, int bytes_to_apply, size_t s, int *check_tweak) {

	//printf("offset: %x\nbytes: %x\n", offset_to_apply, bytes_to_apply);

	//printf("size: %d\n", s);

	if (offset_to_apply <= s) {

		//printf("here\n");

		uint8_t value = buf[offset_to_apply];

		if (value == bytes_to_apply) {
			//printf(">>>>>value is the same<<<<<\n");
			*check_tweak = *check_tweak + 1;
		}

		//printf("original = %d\n", value);

		buf[offset_to_apply] = bytes_to_apply;

		value = buf[offset_to_apply];
		//printf("new = %d\n", value);
		return 0;
	}

	else {
		printf("offset too big?????\n");
		return 1;
	}
}

int apply_changes(unsigned char *buf, char *rom, size_t s) {
	FILE* overwrite = fopen(rom, "wb");
	if (overwrite) {
		fwrite(buf, 1, s, overwrite);
		fclose(overwrite);
		return 0;
	}
	else {
		printf("no such file??\n");
		fclose(overwrite);
		return 1;
	}
}



































