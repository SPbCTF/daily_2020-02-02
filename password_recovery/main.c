#include "stdio.h"
#include "stdlib.h"
#include "string.h"
#include <unistd.h>
#include <termios.h>

struct user {
    char login[64];
    char password[64];
    struct user *next;
    int type;
};
typedef struct user usr;

usr * usr_list;
usr current;

usr * create_user(char *name, char *password, int type){
    usr *new = malloc(sizeof(usr));
    strncpy(new->login, name, 64);
    strncpy(new->password, password, 64);
    new->next = NULL;
    new->type = type;
    return new;
}

usr * get_last_user_entry(){
    if (usr_list == NULL){
        return NULL;
    }
    usr *curr = usr_list;
    while(curr->next != NULL)
        curr = curr->next;
    return curr;
}

void add_user(usr *user){
    usr *last = get_last_user_entry();
    if(last == NULL){
        usr_list = user;
    }else{
        last->next = user;
    }
}

int register_user(){
    char name[256];
    char password[256];
    printf("Enter your name: ");
    fgets(name, 256, stdin);
    printf("Enter your password: ");
    fgets(password, 256, stdin);
    usr *new = create_user(name, password, 0);
    add_user(new);
}

int load_user(char *name) {
    usr * curr = usr_list;
    while(curr != NULL){
        int nlen = strnlen(curr->login, 64);
        strncpy(current.login, name, 64);
        printf("a %s %d\n", curr->login, nlen);
        if(!strncmp(curr->login, name, nlen)){
            strncpy(current.password, curr->password, 64);
            current.type = curr->type;
            return 1;
        }
        curr = curr->next;
    }
    return 0;
}

int login(){
    char user[256];
    char password[256];
    for(int i = 0; i < 3; i++){
        printf("Enter username: ");
        fgets(user, 256,stdin);
        int pl = strlen(user);
        if (user[pl-1] == '\n'){
            user[pl-1] = 0;
        }
        int is_loaded = load_user(user);
        if (!is_loaded){
            printf("There is no such user %s!\r\n", current.login);
            continue;
        }
        printf("Enter password: ");
        fgets(password, 256, stdin);
        pl = strlen(password);
        if (password[pl-1] == '\n'){
            password[pl-1] = 0;
        }
        int ulen = strnlen(current.password, 64);
        if(!strncmp(password, current.password, ulen)){
            return 1;
        }
        puts("Wrong password!\r");
    }
    memset(&current, 0, sizeof(usr));
    return 0;
}



int we_have_telnet = 0;
int raw_enabled = -1;

void clear_screen() {
    printf("\x1B[3J\x1B[H\x1B[2J");
}

void raw_enable() {
    if (raw_enabled == 1) {
        return;
    }
    
    raw_enabled = 1;
    
    struct termios raw;
    if (we_have_telnet || tcgetattr(STDIN_FILENO, &raw) != 0) {
        printf("\xFF\xFB\x01" "\xFF\xFB\x03" "\xFF\xFC\x22");
        return;
    }
    raw.c_lflag &= ~(ECHO | ICANON);
    tcsetattr(STDIN_FILENO, TCSAFLUSH, &raw);
}

void raw_disable() {
    if (raw_enabled == 0) {
        return;
    }
    
    raw_enabled = 0;
    
    struct termios raw;
    if (we_have_telnet || tcgetattr(STDIN_FILENO, &raw) != 0) {
        printf("\xFF\xFC\x01" "\xFF\xFC\x03" "\xFF\xFB\x22");
        if (we_have_telnet) {
            if (getchar() == 0xFF) { 
                getchar(); getchar();
                if (getchar() == 0xFF) { 
                    getchar(); getchar();
                    if (getchar() == 0xFF) {
                        getchar(); getchar();
                    }
                }
            }
        }
        return;
    }
    raw.c_lflag |= (ECHO | ICANON);
    tcsetattr(STDIN_FILENO, TCSAFLUSH, &raw);
}

int read_key() {
    alarm(10);
    
    int key = getchar();
    if (key == EOF) {
        exit(1);
    }
    
    if (key == 0xFF) {
        we_have_telnet = 1;
        getchar();
        getchar();
        
        return read_key();
    }
    
    if (key == '\r') {
        getchar();
        return 10;
    }
    
    return key;
}

int read_allowed_key(int * allowed) {
    int key, i;
    
    while (1) {
        key = read_key();
        
        for (i = 0; allowed[i] != 0; i++) {
            if (key == allowed[i]) {
                return key;
            }
        }
    }
}



int check_sms(){
    puts("Now enter your phone code:\r");
    raw_enable();
    system("./gen_and_send_code.sh");

    char from_user[32];
    char checked[32];
    FILE *rnd = fopen(".code", "r");
    fread(checked, 6, 1, rnd);
    fclose(rnd);
    printf("chec %s\n", checked);
    int entered = 0;
    int idx = 0;
    while(entered < 6){
        int symb = read_key();
        from_user[idx] = (char)symb;
        printf("%d\n", symb);
        if((symb == '\b')||(symb == 127)){
            if(entered != 0){
                putchar('\b');
                putchar(' ');
                putchar('\b');
                entered -= 1;
            }
        }else{
            if((symb < '0') || (symb > '9')){
                from_user[idx] = 0;
                break;
            } 
            putchar('*');
            entered += 1;
        }
        idx += 1;
    }
    putchar('\r');
    putchar('\n');
    raw_disable();
    //(void) tcsetattr (fileno (stdin), TCSAFLUSH, &old);
    printf("chec %s %d\n", checked, atoi(checked));
    if (atoi(from_user) == atoi(checked)){
        return 1;
    }
    return 0;
}

void print_flag(){
    system("cat flag.txt");
    puts("\r");
    puts("WellDone!\r");
}


void load_admin(){
    FILE *adm_pass = fopen(".admin_pass", "rb");
    char password[256];
    fgets(password, 256, adm_pass);
    int pl = strlen(password);
    if (password[pl-1] == '\n'){
        password[pl-1] = 0;
    }
    fclose(adm_pass);
    usr *new = create_user("yzh_02022017", password, 1);
    add_user(new);
}

int main(int argc, char **argv){
    setvbuf(stdout, 0, 2, 0);
    setvbuf(stdin , 0, _IONBF, 0);
    load_admin();
    char input[256];
    puts("*********************************************************\r\n* Welcome to your personal bank account control system! *\r\n*********************************************************\r");
    while(1){
        puts("menu:\r\n reg - register\r\n login - login\r");
        fgets(input, 256, stdin);
        int last = strlen(input)-1;
        while((input[last] == '\r') || (input[last] == '\n')){
            input[last] = 0;
            last--;
        }
        if(!strcmp(input, "reg")){
            register_user();
            puts("registered");
        }else if (!strcmp(input, "login")){
            if (login() == 1){
                if(current.type == 1){
                    if(check_sms() == 1) {
                        puts("Ok! here your flag: \r");
                        print_flag();
                        return 1;
                    }else{
                        puts("Wrong code! Bye!\r");
                        return 0;
                    }
                }else{
                    puts("you are not priv user! this part not implemented yet...\r");
                }
            }else{
                puts("Wrong login!\r");
                break;
            }
        }else{
            puts("Bye!\r");
            break;
        }
    }
    return 0;

}