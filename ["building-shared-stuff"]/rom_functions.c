#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <stdlib.h>

int check_tweak(char* rom, char* offset, char* bytes) {
	
	FILE* f = fopen(rom, "rb");
	if (f) {
		int bytes_to_check;
		sscanf(bytes, "%x", &bytes_to_check);

		int offset_to_check;
		sscanf(offset, "%x", &offset_to_check);

		//goes to the end of the file to find out the size
		fseek(f,0,SEEK_END);
		size_t size = ftell(f);	//64 bit or 32 bit depending on system

		//put the cursor back to the start of the rom
		rewind(f);

		//create the array to hold the rom
		unsigned char* buf = malloc(size);

		//put the data into the array
		fread(buf, 1, size, f);

		//close the file
		fclose(f);
	
		//get the number at the offset
		uint8_t val;
		val = *(uint8_t*)(buf + offset_to_check);

		free(buf);

		if (val == bytes_to_check) {
			return 1;
		}
		else {
			return 0;
		}

	}
	return -1;

}





int apply_tweak(char* rom, char* offset, char* bytes) {

	//open the rom
	FILE* f = fopen(rom, "rb");
	if (f) {
		printf("%s, %s, %s\n", rom, offset, bytes);

		//goes to the end of the file to find out the size
		fseek(f,0,SEEK_END);
		size_t size = ftell(f);	//64 bit or 32 bit depending on system

		//put the cursor back to the start of the rom
		rewind(f);

		//create the array to hold the rom
		unsigned char* buf = malloc(size);

		//put the data into the array
		fread(buf, 1, size, f);

		//close the file
		fclose(f);


		int offset_to_apply;
		sscanf(offset, "%x", &offset_to_apply);
		printf("%d\n", offset_to_apply);

		printf("%s\n", bytes);
//			printf("%s\n", bytes[i]);
//			printf("%s\n", bytes[i+1]);

		//turns the strings into decimal integers
		int byte_to_apply;
		sscanf(bytes, "%x", &byte_to_apply);

		//apply a number to the given offset
		*(uint8_t*)(buf + offset_to_apply) = byte_to_apply;

		//open the file again but this time to write to it
		FILE* out = fopen("rom.smc", "wb");
		if (out) {
			//overwrite the rom with the new version of it
			fwrite(buf, 1, size, out);

			//close the file
			fclose(out);
		}
	
		//free the memory used for the array
		free(buf);

	}
	return 0;
}


















