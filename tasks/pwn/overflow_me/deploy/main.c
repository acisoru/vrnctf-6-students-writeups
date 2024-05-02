#include <stdio.h>
#include <string.h>
#include <stdio.h>

char key_correct[] = "I_HATE_RUS";

int main() {
    setvbuf(stdout, NULL, _IONBF, 0);
	setvbuf(stdin, NULL, _IONBF, 0);

    printf("Инструкции нано-брони (вводить именно сами команды):\n1) Set - активация защиты\n2) Unset - дезактивация защиты\n3) Fire - выброс плазмы в противника\n4)Hide - переход в режим невидимки.\n");

    char check[] = "VRNCTF_MEME";
    char command[10];
    
    while(1) {
        printf(">> ");
        gets(command);

        if(!strcmp(command, "Set")) 
            printf("Activated!\n");
        else if(!strcmp(command, "Unset"))
            printf("Unactivated!\n");
        else if(!strcmp(command, "Fire"))
            printf("Finding target..... Found! Attack!\n");
        else if(!strcmp(command, "Hide"))
            printf("Activated invisible mode!\n");
        else if (strcmp(check, key_correct) == 0) {
            FILE* file = fopen("flag", "r");
            char flag[29];
            fgets(flag, 29, file);
            printf("%s\n", flag);
        }
    }

    return 0;
}
