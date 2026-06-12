#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <iomanip>
#include <sstream>

// Basic SHA-like hashing logic for speed demonstration
// In production, we'd link to OpenSSL for full SHA-256
std::string fast_checksum(const std::string& filepath) {
    std::ifstream file(filepath, std::ios::binary);
    if (!file) return "ERROR";

    unsigned int hash = 0x811c9dc5; // FNV-1a offset basis
    char buffer[65536];
    
    while (file.read(buffer, sizeof(buffer)) || file.gcount() > 0) {
        std::streamsize bytes = file.gcount();
        for (std::streamsize i = 0; i < bytes; ++i) {
            hash ^= static_cast<unsigned char>(buffer[i]);
            hash *= 0x01000193; // FNV-1a prime
        }
    }

    std::stringstream ss;
    ss << std::hex << std::setw(8) << std::setfill('0') << hash;
    return ss.str();
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cout << "Usage: FastHasher <file_path>" << std::endl;
        return 1;
    }

    std::string path = argv[1];
    std::string result = fast_checksum(path);
    std::cout << "RESULT:" << result << std::endl;

    return 0;
}
