 %module rom_functions
 %{
extern int make_changes(unsigned char *, int, int, size_t, int*);
extern int get_data(char *, unsigned char **, FILE *, size_t *);
extern int apply_changes(unsigned char *, char *, size_t);
extern int not_main(char *, char *, char *, int);
%}

extern int make_changes(unsigned char *, int, int, size_t, int*);
extern int get_data(char *, unsigned char **, FILE *, size_t *);
extern int apply_changes(unsigned char *, char *, size_t);
extern int not_main(char *, char *, char *, int);
