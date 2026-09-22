# 부록 F — 전체 실습 파일 트리

실습에 필요한 모든 파일입니다. 함께 전달된 `onprem-lab.zip`을 `~/onprem-lab/`에 풀면 이 구조가 됩니다. 아래 파일 내용은 빌드 시점의 실제 파일에서 자동으로 가져온 것이므로 문서 본문과 어긋나지 않습니다.

## F-1. 디렉터리 구조

```text
{{LAB_TREE}}
```

실습 중 생성되는 것들(`wheels/`, `trivy-cache/`, `day08/certs/`, `*.tar.gz`, `sbom-*.json`, `.env`)은 목록에서 제외했습니다. `.env.example`을 복사해 `.env`를 만드세요.

| 디렉터리 | 내용 | 관련 Day |
|---|---|---|
| `bootstrap.sh` | OS별 도구 설치, 디렉터리 생성, 이미지 미리 받기 | 0 |
| `agent/` | 학습용 에이전트 (한 번 빌드, 계속 재사용). `Dockerfile.ca`는 사내 CA 병합 | 0, 3, 8 |
| `day01/` | Ansible 인벤토리·플레이북 | 1 |
| `day02/` | 네임스페이스·브리지·NAT 실습을 한 번에 만드는 스크립트 | 2 |
| `day03/` | 취약점 스캔 래퍼 | 3 |
| `day04/` | 진단 3단계 스크립트 | 4 |
| `day05/` | 3티어 Compose, nginx, 이미지 밖 설정 | 5 |
| `day06/` | 3존 Compose, 고장 심기(`break.sh`) | 6 |
| `day07/` | 화이트리스트 프록시 | 7 |
| `day08/` | TLS 검사 프록시 + CA 세 가지 해결 | 8 |
| `day09/` | 오프라인 Dockerfile, 레지스트리 + UI | 9 |
| `day10/` | 첫 쿠버네티스 매니페스트, 고장 5종 | 10 |
| `day11/` | ConfigMap/Secret/Ingress, Helm 차트 `ax-agent` | 11 |
| `day12/` | 존 네임스페이스, NetworkPolicy | 12 |
| `day13/` | LiteLLM 게이트웨이 + 감사 DB | 13 |
| `skeleton/` | **첫 케이스에 가져갈 키트**: Compose, k8s(kustomize), verify.sh, RUNBOOK, docs | 14 |

## F-2. 파일 전문

각 항목을 펼치면 전문이 보이고, 코드 블록의 복사 버튼으로 그대로 가져갈 수 있습니다. 학습용 에이전트(`agent/app.py`)는 배포 실습을 위한 더미이며 설명하지 않습니다 — 엔드포인트 목록은 Day 0에 있습니다.

{{LAB_FILES}}
