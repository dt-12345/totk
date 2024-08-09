#!/usr/bin/env python3

import argparse
import hashlib
from pathlib import Path
import subprocess
from typing import Optional
from common import setup_common as setup

TARGET_PATH = setup.get_target_path()
TARGET_ELF_PATH = setup.get_target_elf_path()

def prepare_executable(original_nso: Optional[Path]):
    COMPRESSED_V121_HASH = "e5aa8d48e68cbb82ed4416c7b6b29a46fe4a998ee149d6dbf979164c628efcb6"
    UNCOMPRESSED_V121_HASH = "6424f89c32020bac0053e919360652b9ccbb2420031ab3ccc2425839ffdf6461"

    # The uncompressed v1.2.1 main NSO
    TARGET_HASH = UNCOMPRESSED_V121_HASH

    if TARGET_PATH.is_file() and hashlib.sha256(TARGET_PATH.read_bytes()).hexdigest() == TARGET_HASH and TARGET_ELF_PATH.is_file():
        print(">>> NSO is already set up")
        return
    
    if not original_nso.is_file():
        setup.fail(f"{original_nso} is not a file")

    nso_data = original_nso.read_bytes()
    nso_hash = hashlib.sha256(nso_data).hexdigest()

    if nso_hash == UNCOMPRESSED_V121_HASH:
        print(">>> found uncompressed 1.2.1 NSO")
        TARGET_PATH.write_bytes(nso_data)

    elif nso_hash == COMPRESSED_V121_HASH:
        print(">>> found compressed 1.2.1 NSO")
        setup._decompress_nso(original_nso, TARGET_PATH)

    else:
        setup.fail(f"Unknown executable: {nso_hash}")

    if not TARGET_PATH.is_file():
        setup.fail("internal error while preparing executable (missing NSO); please report")
    if hashlib.sha256(TARGET_PATH.read_bytes()).hexdigest() != TARGET_HASH:
        setup.fail("internal error while preparing executable (wrong NSO hash); please report")

    setup._convert_nso_to_elf(TARGET_PATH)

    if not TARGET_ELF_PATH.is_file():
        setup.fail("internal error while preparing executable (missing ELF); please report")

def create_build_dir():
    build_dir = setup.ROOT / "build"
    if build_dir.is_dir():
        print(">>> build directory already exists: nothing to do")
        return

    subprocess.check_call(
        "cmake -GNinja -DCMAKE_BUILD_TYPE=RelWithDebInfo -DCMAKE_TOOLCHAIN_FILE=toolchain/ToolchainNX64.cmake -DCMAKE_CXX_COMPILER_LAUNCHER=ccache -B build/".split(" "))
    print(">>> created build directory")

def main():
    parser = argparse.ArgumentParser(
        "setup.py", description="Set up the Tears of the Kingdom decompilation project")
    parser.add_argument("original_nso", type=Path,
                        help="Path to the original NSO (1.2.1, compressed or not)", nargs="?")
    args = parser.parse_args()

    setup.install_viking()
    prepare_executable(args.original_nso)
    setup.set_up_compiler("14.0.0")
    create_build_dir()


if __name__ == "__main__":
    main()