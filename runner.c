#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main(int argc, char **argv){
    if(argc < 2){
        printf("Usage: ./runner <file.rasm>.\n");
        return 1;
    }

    char command[1024] = "python runner.py";

    for(int i = 1; i < argc; i++){
        strcat(command, " ");
        strcat(command, argv[i]);
    }

    printf("%s.\n", command);
    system(command);
    return 0;
}