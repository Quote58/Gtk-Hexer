 %module rom_functions
 %{
extern int apply_tweak(char* rom, char* offset, char* bytes);
extern int check_tweak(char* rom, char* offset, char* bytes);
extern void setup_rom(FILE* f, char** buf, size_t *size, int *offset_to_apply, int *bytes_to_apply, char *offset, char *bytes);
%}

extern int apply_tweak(char* rom, char* offset, char* bytes);
extern int check_tweak(char* rom, char* offset, char* bytes);
extern void setup_rom(FILE* f, char** buf, size_t *size, int *offset_to_apply, int *bytes_to_apply, char *offset, char *bytes);
