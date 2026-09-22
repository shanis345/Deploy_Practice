#!/usr/bin/env bash
# Day 3 실습 3-3: 취약점 스캔 래퍼. 사용법: ./scan.sh <이미지> [--ignore-unfixed]
set -u
IMG="${1:?이미지 이름}"; shift || true
DIR="$(cd "$(dirname "$0")" && pwd)"
mkdir -p "$DIR/trivy-cache"
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock -v "$DIR/trivy-cache:/root/.cache/" \
  aquasec/trivy:0.56.2 image --severity HIGH,CRITICAL --scanners vuln "$@" "$IMG"
