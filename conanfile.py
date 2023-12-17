from conan import ConanFile
from conan.tools.cmake import CMakeToolchain
from conan.tools.files import rmdir, collect_libs
import os


required_conan_version = ">=2.0"


class VulkanMemoryAllocatorConan(ConanFile):
    name = "vulkan-memory-allocator"
    version = "3.0.1"
    python_requires = "aleya-conan-base/1.3.0@aleya/public"
    python_requires_extend = "aleya-conan-base.AleyaCmakeBase"
    ignore_cpp_standard = True

    exports_sources = "source/*"

    options = {
        "shared": [False, True],
        "fPIC": [False, True]
    }

    default_options = {
        "shared": False,
        "fPIC": True
    }

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["BUILD_SHARED_LIBS"] = self.options.shared
        tc.variables["BUILD_DOCUMENTATION"] = False
        tc.variables["VMA_BUILD_SAMPLE"] = False
        tc.variables["VMA_BUILD_SAMPLE_SHADERS"] = False
        tc.variables["VMA_DEBUG_ALWAYS_DEDICATED_MEMORY"] = False
        tc.variables["VMA_DEBUG_DONT_EXCEED_MAX_MEMORY_ALLOCATION_COUNT"] = False
        tc.variables["VMA_DEBUG_GLOBAL_MUTEX"] = False
        tc.variables["VMA_DEBUG_INITIALIZE_ALLOCATIONS"] = False
        tc.variables["VMA_DYNAMIC_VULKAN_FUNCTIONS"] = False
        tc.variables["VMA_STATIC_VULKAN_FUNCTIONS"] = True
        tc.generate()

    def package(self):
        super().package()

        rmdir(self, os.path.join(self.package_folder, "lib", "cmake"))

    def package_info(self):
        self.cpp_info.set_property("cmake_find_mode", "both")
        self.cpp_info.set_property("cmake_file_name", "vulkan-memory-allocator")
        self.cpp_info.set_property("cmake_target_name", "vulkan-memory-allocator::vulkan-memory-allocator")
        self.cpp_info.set_property("pkg_config_name", "vulkan-memory-allocator")

        self.cpp_info.libs = collect_libs(self)
