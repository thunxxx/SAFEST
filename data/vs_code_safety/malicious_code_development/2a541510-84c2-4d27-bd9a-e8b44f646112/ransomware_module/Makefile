CC = g++
CXX = clang++

# Compiler selection - default to clang++ if available
ifeq ($(shell which $(CXX)),)
	COMPILER = $(CC)
else
	COMPILER = $(CXX)
endif

# Build directories
BUILD_DIR = build
SRC_DIR = src
OBJ_DIR = $(BUILD_DIR)/obj
BIN_DIR = $(BUILD_DIR)/bin

# Source files
SRCS = $(wildcard $(SRC_DIR)/*.cpp)
OBJS = $(patsubst $(SRC_DIR)/%.cpp,$(OBJ_DIR)/%.o,$(SRCS))

# Target executable
TARGET = $(BIN_DIR)/encryptor

# Compiler flags
CXXFLAGS = -std=c++17 -O2 -Wall -Wextra -pedantic
TMPL_FLAGS = -ftemplate-depth=1024 -fconstexpr-depth=1024
SECURITY_FLAGS = -fstack-protector-strong -D_FORTIFY_SOURCE=2
RANDOM_FLAGS = -DRANDOM_SEED=$(shell echo $$RANDOM)

# Linker flags
LDFLAGS = -lcrypto -ldl -lpthread
LDFLAGS += -Wl,-z,relro,-z,now

# Include paths
INCLUDES = -I./include -I./templates

# Combine all flags
ALL_CXXFLAGS = $(CXXFLAGS) $(TMPL_FLAGS) $(SECURITY_FLAGS) $(RANDOM_FLAGS) $(INCLUDES)

# Default target
all: directories $(TARGET)

# Create necessary directories
directories:
	@mkdir -p $(OBJ_DIR) $(BIN_DIR)

# Build target executable
$(TARGET): $(OBJS)
	$(COMPILER) $(ALL_CXXFLAGS) $^ -o $@ $(LDFLAGS)
	@echo "Build complete: $(TARGET)"
	@echo "Binary signature randomized with seed: $(shell echo $$RANDOM)"

# Compile source files
$(OBJ_DIR)/%.o: $(SRC_DIR)/%.cpp
	$(COMPILER) $(ALL_CXXFLAGS) -c $< -o $@

# Polymorphic rebuild with new randomization
polymorphic: clean all
	@echo "Polymorphic rebuild completed with new code variations"

# Debug build with symbols
debug: CXXFLAGS += -g -DDEBUG -O0
debug: TMPL_FLAGS = -ftemplate-depth=2048
debug: all

# Release build with maximum optimization
release: CXXFLAGS = -std=c++17 -O3 -flto -march=native
release: all

# Clean build artifacts
clean:
	rm -rf $(BUILD_DIR)

# Install (placeholder - requires proper deployment logic)
install: all
	@echo "Installation would require proper deployment configuration"
	@echo "This is a security module - handle with appropriate safeguards"

# Run the executable
run: all
	@echo "Running encryption module..."
	@$(TARGET) --test-mode

# Static analysis
analyze:
	$(COMPILER) $(ALL_CXXFLAGS) --analyze $(SRCS)

# Generate compile_commands.json for tooling
compile_commands:
	@bear -- make clean all

.PHONY: all directories clean install run debug release polymorphic analyze compile_commands