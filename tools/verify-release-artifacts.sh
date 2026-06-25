#!/usr/bin/env sh
set -eu

repo_root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
install_dir="$repo_root/install"

fail() {
  echo "ERROR: $*" >&2
  exit 1
}

need_cmd() {
  command -v "$1" >/dev/null 2>&1 || fail "missing required command: $1"
}

need_cmd md5sum
need_cmd sha256sum
need_cmd tar
need_cmd od

is_elf() {
  # ELF magic: 7f 45 4c 46. Use od for BusyBox/Coreutils portability.
  [ "$(od -An -tx1 -N4 "$1" | tr -d ' \n')" = "7f454c46" ]
}

check_md5_file() {
  file=$1
  checksum_file=$2
  expected=$(tr -d ' \r\n' < "$checksum_file")
  actual=$(md5sum "$file" | awk '{print $1}')
  [ "$expected" = "$actual" ] || fail "MD5 mismatch: $file"
}

[ -d "$install_dir" ] || fail "missing install directory: $install_dir"

for dir in "$install_dir"/[0-9]*; do
  [ -d "$dir" ] || continue
  version=${dir##*/}
  bin="$dir/zerotier-one"
  tarball="$dir/zerotier.tar.gz"

  [ -s "$bin" ] || fail "missing binary: $bin"
  [ -s "$tarball" ] || fail "missing tarball: $tarball"
  [ -s "$dir/MD5.txt" ] || fail "missing binary MD5: $dir/MD5.txt"
  [ -s "$dir/tarMD5.txt" ] || fail "missing tarball MD5: $dir/tarMD5.txt"

  is_elf "$bin" || fail "not an ELF binary: $bin"
  check_md5_file "$bin" "$dir/MD5.txt"
  check_md5_file "$tarball" "$dir/tarMD5.txt"
  tar -tzf "$tarball" >/dev/null || fail "invalid tarball: $tarball"

  tmpdir=$(mktemp -d)
  trap 'rm -rf "$tmpdir"' EXIT HUP INT TERM
  tar -xzf "$tarball" -C "$tmpdir"
  extracted=$(find "$tmpdir" -type f -name zerotier-one | head -n 1)
  [ -n "$extracted" ] || fail "tarball does not contain zerotier-one: $tarball"
  is_elf "$extracted" || fail "tarball zerotier-one is not ELF: $tarball"
  rm -rf "$tmpdir"
  trap - EXIT HUP INT TERM

  echo "OK: $version"
done

if [ -s "$install_dir/SHA256SUMS" ]; then
  (cd "$install_dir" && sha256sum -c SHA256SUMS)
fi
