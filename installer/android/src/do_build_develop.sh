#!/bin/sh

set -eu

missing_system_dependency=0
for command in git zip unzip java javac pip3 virtualenv autoconf libtoolize pkg-config cmake automake autopoint gettext; do
    if ! command -v "$command" >/dev/null 2>&1; then
        missing_system_dependency=1
    fi
done

if [ "$missing_system_dependency" -eq 1 ]; then
    sudo apt update
    sudo apt install -y git zip unzip openjdk-17-jdk python3-pip python3-virtualenv autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo6 cmake libffi-dev libssl-dev automake autopoint gettext
fi

curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- --default-toolchain none -y

rustup toolchain install nightly --allow-downgrade --profile minimal --component clippy

. "$HOME/.cargo/env"

# rm -rf "$HOME/.buildozer/android/platform/android-ndk-*"

# rm -rf .buildozer

# The Python 3.12 build script wrapped the NDK compilers to inject a grp.h
# shim that no longer exists; put the original compilers back.
NDK_COMPILER_DIR="$HOME/.buildozer/android/platform/android-ndk-r27/toolchains/llvm/prebuilt/linux-x86_64/bin"
for real_compiler in "$NDK_COMPILER_DIR"/*-clang.real; do
    if [ -e "$real_compiler" ]; then
        mv -f "$real_compiler" "${real_compiler%.real}"
    fi
done

# A build left over from the Python 3.12 pin would be reused by p4a as-is,
# and its stdlib modules are not linked against libpython.
BUILD_PLATFORM_DIR="$PWD/../cache/.buildozer/android/platform"
if find "$BUILD_PLATFORM_DIR" -path "*/build-*" -name 'libpython3.12.so' -print 2>/dev/null | grep -q .; then
    rm -rf "$BUILD_PLATFORM_DIR"/build-*
fi

VENV="venv_p4a_develop_py314"

# rm -rf "${VENV}"

python3.14 -m venv "${VENV}"

. "${VENV}/bin/activate"

pip install git+https://github.com/kivy/buildozer

pip install legacy-cgi setuptools 'cython>=3.1,<3.4'

unset CPATH C_INCLUDE_PATH CPLUS_INCLUDE_PATH CPPFLAGS CFLAGS CXXFLAGS LDFLAGS

# Kivy's SDL probe must not import host SDL pkg-config flags into an NDK build.
BUILD_TOOLS_DIR="$PWD/.buildozer-build-tools"
rm -rf .buildozer-build-tools
mkdir -p "$BUILD_TOOLS_DIR"
trap 'rm -rf .buildozer-build-tools' EXIT HUP INT TERM

cat > "$BUILD_TOOLS_DIR/pkg-config" <<'EOF'
#!/bin/sh

case " $* " in
    *" sdl2 "*|*" SDL2_ttf "*|*" SDL2_image "*|*" SDL2_mixer "*)
        exit 1
        ;;
esac

exec /usr/bin/pkg-config "$@"
EOF
chmod +x "$BUILD_TOOLS_DIR/pkg-config"

env \
    -u CPATH \
    -u C_INCLUDE_PATH \
    -u CPLUS_INCLUDE_PATH \
    -u CFLAGS \
    -u CPPFLAGS \
    -u CXXFLAGS \
    -u LDFLAGS \
    PATH="$BUILD_TOOLS_DIR:$PATH" \
    PKG_CONFIG_PATH=/nonexistent \
    PKG_CONFIG_LIBDIR=/nonexistent \
    PIP_NO_BINARY="charset-normalizer,chardet" \
    buildozer android debug
