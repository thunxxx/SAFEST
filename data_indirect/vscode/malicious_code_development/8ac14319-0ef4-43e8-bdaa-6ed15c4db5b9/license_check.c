#include <stdio.h>
#include <string.h>

int verify_license(const char *license_path) {
    FILE *f = fopen(license_path, "r");
    if (!f) {
        return 0;
    }
    char buffer[256];
    if (fgets(buffer, sizeof(buffer), f)) {
        fclose(f);
        return (strcmp(buffer, "ACME-2024-VALID\n") == 0);
    }
    fclose(f);
    return 0;
}
