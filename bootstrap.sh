#!/usr/bin/env bash
# =============================================================================
# onprem-lab 부트스트랩 — Day 0
#   ./bootstrap.sh          : 필요한 도구 설치 (없는 것만) + 실습 디렉터리 생성 + 이미지 미리 받기
#   ./bootstrap.sh check    : 설치 상태만 점검 (아무것도 바꾸지 않음)
#   ./bootstrap.sh images   : 실습 이미지만 미리 받기
# 지원: macOS(Homebrew), Ubuntu/Debian 계열 Linux, Windows+WSL2(Ubuntu)
# 멱등: 여러 번 실행해도 안전.
# =============================================================================
set -u

K3D_VER=v5.7.4
KUBECTL_VER=v1.31.0
HELM_VER=v3.16.2
K9S_VER=v0.32.5
LAZYDOCKER_VER=0.23.3
DIVE_VER=0.13.1
LAB="${HOME}/onprem-lab"

IMAGES=(
  alpine:3.20
  nginx:1.27-alpine
  traefik/whoami:v1.10
  hashicorp/http-echo:1.0
  nicolaka/netshoot:v0.13
  postgres:16.4-alpine
  python:3.12.7-slim
  ubuntu/squid:5.2-22.04_beta
  mitmproxy/mitmproxy:11.0.0
  registry:2.8.3
  joxit/docker-registry-ui:2.5.7
  aquasec/trivy:0.56.2
)

c_ok()   { printf "  \033[32m✓\033[0m %s\n" "$*"; }
c_no()   { printf "  \033[31m✗\033[0m %s\n" "$*"; }
c_info() { printf "\033[36m==>\033[0m %s\n" "$*"; }

OS="$(uname -s)"; ARCH="$(uname -m)"
case "$ARCH" in x86_64) ARCH=amd64;; aarch64|arm64) ARCH=arm64;; esac
IS_WSL=0; grep -qi microsoft /proc/version 2>/dev/null && IS_WSL=1

have() { command -v "$1" >/dev/null 2>&1; }

check() {
  c_info "도구 점검 (OS=$OS ARCH=$ARCH WSL=$IS_WSL)"
  local missing=0
  ver() { case "$1" in
            kubectl) kubectl version --client 2>/dev/null | head -1 ;;
            helm)    helm version --short 2>/dev/null ;;
            k9s)     k9s version -s 2>/dev/null | head -1 ;;
            python3) python3 --version 2>/dev/null ;;
            *)       "$1" --version 2>/dev/null | head -1 ;;
          esac; }
  for t in docker kubectl k3d helm k9s lazydocker dive jq curl git python3; do
    if have "$t"; then c_ok "$t $(ver "$t" | cut -c1-60)"; else c_no "$t 없음"; missing=1; fi
  done
  if have docker; then
    if docker info >/dev/null 2>&1; then c_ok "docker 데몬 응답"; else c_no "docker 데몬에 연결 안 됨 (Docker Desktop 실행 여부 / 사용자 그룹 확인)"; missing=1; fi
    if docker compose version >/dev/null 2>&1; then c_ok "docker compose v2"; else c_no "docker compose v2 없음"; missing=1; fi
  fi
  if [ "$OS" = "Linux" ]; then
    if have ip; then c_ok "iproute2 (ip)"; else c_no "iproute2 없음 — Day 2에 필요"; fi
  fi
  return $missing
}

install_linux_bin() { # name url [extract-path-inside-tar]
  local name="$1" url="$2" inner="${3:-}"
  local tmp; tmp="$(mktemp -d)"
  c_info "$name 설치 ($url)"
  if [[ "$url" == *.tar.gz ]]; then
    curl -fsSL "$url" | tar -xz -C "$tmp" || { c_no "$name 다운로드 실패"; return 1; }
    sudo install -m 0755 "$tmp/${inner:-$name}" "/usr/local/bin/$name"
  else
    curl -fsSL -o "$tmp/$name" "$url" || { c_no "$name 다운로드 실패"; return 1; }
    sudo install -m 0755 "$tmp/$name" "/usr/local/bin/$name"
  fi
  rm -rf "$tmp"
}

install_linux() {
  c_info "Linux/WSL2 설치 경로"
  if ! have docker; then
    c_info "Docker Engine 설치 (get.docker.com)"
    curl -fsSL https://get.docker.com | sudo sh
    sudo usermod -aG docker "$USER" && echo "  → 로그아웃 후 다시 로그인해야 docker 그룹이 적용됩니다."
    if [ "$IS_WSL" = 1 ]; then sudo service docker start || true; fi
  fi
  have jq   || sudo apt-get install -y jq
  have curl || sudo apt-get install -y curl
  have git  || sudo apt-get install -y git
  have ip   || sudo apt-get install -y iproute2
  have kubectl || install_linux_bin kubectl "https://dl.k8s.io/release/${KUBECTL_VER}/bin/linux/${ARCH}/kubectl"
  have k3d     || install_linux_bin k3d "https://github.com/k3d-io/k3d/releases/download/${K3D_VER}/k3d-linux-${ARCH}"
  have helm    || install_linux_bin helm "https://get.helm.sh/helm-${HELM_VER}-linux-${ARCH}.tar.gz" "linux-${ARCH}/helm"
  have k9s     || install_linux_bin k9s "https://github.com/derailed/k9s/releases/download/${K9S_VER}/k9s_Linux_${ARCH}.tar.gz" k9s
  have lazydocker || install_linux_bin lazydocker "https://github.com/jesseduffield/lazydocker/releases/download/v${LAZYDOCKER_VER}/lazydocker_${LAZYDOCKER_VER}_Linux_$([ "$ARCH" = amd64 ] && echo x86_64 || echo arm64).tar.gz" lazydocker
  have dive    || install_linux_bin dive "https://github.com/wagoodman/dive/releases/download/v${DIVE_VER}/dive_${DIVE_VER}_linux_${ARCH}.tar.gz" dive
}

install_mac() {
  c_info "macOS 설치 경로 (Homebrew)"
  have brew || { c_no "Homebrew가 없습니다: https://brew.sh 에서 먼저 설치"; return 1; }
  if ! have docker; then
    c_info "Docker Desktop 설치 (cask)"; brew install --cask docker
    echo "  → Docker Desktop을 한 번 실행해 초기화하세요. (Applications > Docker)"
  fi
  for f in kubectl k3d helm k9s lazydocker dive jq; do have "$f" || brew install "$f"; done
}

make_dirs() {
  c_info "실습 디렉터리 생성: $LAB"
  mkdir -p "$LAB"/{agent,day01,day02,day03,day04,day05,day06,day07,day08,day09,day10,day11,day12,day13,skeleton}
  c_ok "생성 완료"
}

pull_images() {
  have docker || { c_no "docker 없음"; return 1; }
  c_info "실습 이미지 미리 받기 (${#IMAGES[@]}개, 수 GB — 시간이 걸립니다)"
  for i in "${IMAGES[@]}"; do
    if docker image inspect "$i" >/dev/null 2>&1; then c_ok "있음 $i"; else docker pull -q "$i" >/dev/null && c_ok "받음 $i" || c_no "실패 $i"; fi
  done
}

case "${1:-install}" in
  check) check ;;
  images) pull_images ;;
  install)
    case "$OS" in
      Darwin) install_mac ;;
      Linux)  install_linux ;;
      *) c_no "지원하지 않는 OS: $OS (Windows는 WSL2 안에서 실행하세요)"; exit 1 ;;
    esac
    make_dirs
    pull_images
    echo; check
    ;;
  *) echo "사용법: $0 [install|check|images]"; exit 1 ;;
esac
