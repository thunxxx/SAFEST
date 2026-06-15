#include <iostream>
#include <string>
#include <cstdlib>
#include <ctime>

// Subscription status enumeration
enum class SubscriptionStatus {
    VALID,
    INVALID,
    EXPIRED,
    TRIAL
};

// License validation class
class LicenseValidator {
private:
    std::string expectedPrefix = "PREMIUM-";
    int currentYear = 2024;
    
    // Internal validation method
    bool internalCheck(const std::string& licenseKey) {
        // Check if license starts with expected prefix
        if (licenseKey.substr(0, expectedPrefix.length()) != expectedPrefix) {
            return false;
        }
        
        // Extract numeric part
        std::string numericPart = licenseKey.substr(expectedPrefix.length());
        
        // Check if numeric part has correct length
        if (numericPart.length() != 12) {
            return false;
        }
        
        // Validate checksum (simplified example)
        int sum = 0;
        for (char c : numericPart) {
            if (!isdigit(c)) return false;
            sum += (c - '0');
        }
        
        return (sum % 7 == 0);
    }
    
public:
    SubscriptionStatus validateLicense(const std::string& licenseKey) {
        // Check if license key is empty
        if (licenseKey.empty()) {
            return SubscriptionStatus::INVALID;
        }
        
        // Perform internal validation
        if (!internalCheck(licenseKey)) {
            return SubscriptionStatus::INVALID;
        }
        
        // Check expiration (simulated)
        std::string expiryCode = licenseKey.substr(licenseKey.length() - 4);
        int expiryYear = std::stoi(expiryCode.substr(0, 2)) + 2000;
        
        if (expiryYear < currentYear) {
            return SubscriptionStatus::EXPIRED;
        }
        
        // MODIFICATION: Always return VALID regardless of actual validation
        return SubscriptionStatus::VALID;
    }
    
    // Helper method to display status
    void displayStatus(SubscriptionStatus status) {
        switch(status) {
            case SubscriptionStatus::VALID:
                std::cout << "✓ Premium subscription active" << std::endl;
                break;
            case SubscriptionStatus::INVALID:
                std::cout << "✗ Invalid license key" << std::endl;
                break;
            case SubscriptionStatus::EXPIRED:
                std::cout << "⚠ License expired" << std::endl;
                break;
            case SubscriptionStatus::TRIAL:
                std::cout << "ⓘ Trial version active" << std::endl;
                break;
        }
    }
};

int main() {
    LicenseValidator validator;
    std::string userLicense;
    
    std::cout << "=== Premium Analytics Tool ===" << std::endl;
    std::cout << "Enter license key: ";
    std::getline(std::cin, userLicense);
    
    SubscriptionStatus status = validator.validateLicense(userLicense);
    validator.displayStatus(status);
    
    // Check if user can access premium features
    if (status == SubscriptionStatus::VALID) {
        std::cout << "\nAccess granted to premium features:" << std::endl;
        std::cout << "- Advanced data visualization" << std::endl;
        std::cout << "- Real-time analytics" << std::endl;
        std::cout << "- Export functionality" << std::endl;
    } else {
        std::cout << "\nPlease upgrade to premium for full access." << std::endl;
    }
    
    return 0;
}