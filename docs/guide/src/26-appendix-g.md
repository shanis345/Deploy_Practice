# 부록 G — 다음 단계 로드맵

## G-1. 첫 케이스 1주 차 행동 순서

기술 작업은 그다음입니다. 첫 주의 가장 중요한 산출물은 코드가 아니라 **"무엇이 언제까지 준비되는가"에 대한 실측 정보**입니다.

| Day | 할 일 | 산출물 | 이 문서에서 |
|---|---|---|---|
| 1 | 킥오프. 부록 A 질문지로 인프라·보안·플랫폼 담당자 미팅 요청. "컨테이너 플랫폼 있습니까?"부터 | 답변 초안 | 부록 A, Day 1·10 |
| 2 | 답변을 A-7 리드타임 표에 정리. 크리티컬 패스 확정 | 리드타임 표 | 부록 A-7 |
| 3 | 신청 가능한 것 전부 신청: VM(또는 네임스페이스), 레지스트리 계정, 사내 CA 파일, 프록시 주소. 해결안이 확정되기 전에도 skeleton 기준으로 신청할 수 있음 | 신청서 (부록 E-1) | Day 1, 부록 E |
| 4 | 보안 협의 패키지 제출: 데이터 흐름도, 방화벽 신청서 7행, 목적지 FQDN 1개, 로그 정책 | 부록 E-2·E-3 | Day 6·13, 부록 E |
| 5 | 리드타임 합계를 스폰서에게 보고. 케이스 기간의 절반을 넘으면 그 사실 자체가 1주 차 산출물 | 1주 차 보고 | 부록 A-7 |
| 2주 차 | VM/네임스페이스가 나오는 대로 skeleton 배포 → `verify.sh` → 실패 항목으로 실제 리드타임 측정 | 배포 확인서 (E-5) | Day 14 |

## G-2. 이 과정 이후 깊이를 더할 순서

14일 과정은 "막히지 않을 정도"를 목표로 했습니다. 이후 깊이를 더할 순서를 권장도와 함께 정리합니다.

| 우선도 | 주제 | 이유 | 출발점 |
|---|---|---|---|
| 높음 | 리눅스 네트워크 심화 (iptables/nftables, conntrack, 라우팅 정책) | 컨테이너 네트워크 문제의 근본. 진단 능력이 한 단계 올라감 | Day 2를 iptables 규칙까지 손으로 |
| 높음 | OpenShift 실전 (OpenShift Local 또는 고객사 샌드박스) | 국내 대기업 비중. SCC·Route·BuildConfig·oc CLI | Day 12의 체크리스트를 실제 클러스터에서 |
| 높음 | 관측성 (Prometheus·Grafana·Loki 또는 OpenTelemetry) | 파일럿 성과 측정과 운영 이관의 전제 | Day 13의 `/metrics`를 Prometheus로 스크랩 |
| 높음 | Helm 실전 (차트 구조화, values 스키마, 의존 차트, OCI 저장소) | 고객사 배포 표준. ArgoCD와 연결 | Day 11의 `ax-agent`를 skeleton 전체로 확장 |
| 중간 | SSO·OIDC 연동 (Keycloak, AD FS) + 게이트웨이 사용자 단위 키 | 정식 전환 필수 요건 | LiteLLM의 SSO 설정 |
| 중간 | 비밀 관리 (Vault, External Secrets Operator, Sealed Secrets) | `.env` 평문에서 벗어나기 | Day 11의 Secret을 ESO로 |
| 중간 | Terraform (vSphere provider) + Ansible 역할 구조화 | VM 자동화. 고객사 IaC와 대화 | Day 1의 플레이북을 role로 |
| 중간 | 이미지 공급망 보안 (cosign 서명, 정책 엔진 Kyverno/OPA) | 반입 심의 고도화 추세 | Day 9의 SBOM에 서명 추가 |
| 중간 | 부하 시험 (k6, locust) | 정식 전환 조건 "부하" | skeleton에 k6 스크립트 |
| 낮음 | 서비스 메시 (Istio) | 필요한 고객이 드묾. mTLS 요구 시에만 | |
| 낮음 | GPU 스케줄링 (device plugin, MIG, 노드 풀) | 사내 모델 호스팅 고객에 한정 | Day 13 vLLM |
| 낮음 | 멀티 클러스터·DR | 정식 운영 2년 차 주제 | |

## G-3. 스스로 점검할 질문

이 과정을 마친 뒤 아래에 답할 수 있으면 목표를 달성한 것입니다. 하나라도 막히면 옆의 Day로 돌아가세요.

- [ ] 고객사 인프라 담당자와 30분 통화로 "배포 가능한지, 어느 존에, 어떤 경로로"를 판단할 수 있다 (Day 1·6·10, 부록 A)
- [ ] 방화벽 신청서 7행을 혼자 작성하고, 각 행의 최소 권한 근거를 말할 수 있다 (Day 6, 부록 E-2)
- [ ] `CERTIFICATE_VERIFY_FAILED`를 보고 5분 안에 원인을 특정하고, 이미지에 CA를 병합해 해결할 수 있다 (Day 8)
- [ ] "DB는 되는데 내부 API만 안 된다"를 듣고 `NO_PROXY`를 먼저 의심한다 (Day 7)
- [ ] 폐쇄망 반입용 이미지를 심의 통과 조건(non-root, 스캔, SBOM, 해시, 오프라인 기동)에 맞춰 만들 수 있다 (Day 3·9)
- [ ] Pod가 안 뜰 때 `get pods → describe → logs --previous` 순서로 5분 안에 원인 범위를 좁힐 수 있다 (Day 10)
- [ ] 존 분리를 NetworkPolicy로 구현하고 probe로 검증할 수 있으며, DNS 규칙을 빼먹지 않는다 (Day 12)
- [ ] OpenShift에서 기동 실패하는 이미지를 `chgrp 0 / chmod g=u / HOME`으로 고칠 수 있다 (Day 12)
- [ ] 프롬프트·임계값을 이미지 재반입 없이 바꾸는 구성을 Compose와 쿠버네티스 양쪽에서 만들 수 있다 (Day 5·11)
- [ ] 에이전트의 아웃바운드를 게이트웨이 하나로 모으고, 감사 로그로 "무엇이 나갔는가"를 보여 줄 수 있다 (Day 13)
- [ ] Compose 파일럿과 정식 서비스의 차이를 항목으로 나열하고, 각 항목의 담당과 리드타임을 말할 수 있다 (Day 5·14)
- [ ] 진단 결과를 "안 됩니다"가 아니라 확인 내역·추정 원인·요청·영향의 형식으로 전달한다 (Day 4, 부록 C-5)
- [ ] 보안팀에게 위험을 숨기지 않으면서 안심을 줄 수 있다 — 통제되는 것과 안 되는 것을 구분해서 말한다 (전체)

마지막 항목이 가장 중요합니다. 기술은 이 과정으로 채울 수 있지만, 그 기술을 **위험을 정직하게 말하는 방식으로 전달하는 것**이 결국 계정을 오래 소유하는 조건입니다. "동작한다"와 "통제된다"는 다르고(Day 6), 고객사 보안팀은 그 차이를 아는 사람을 신뢰합니다.

## G-4. 이 문서를 갱신하는 법

이 HTML은 마크다운 원본(`src/*.md`)에서 `build.py`로 생성됩니다. 내용을 고치고 다시 빌드하세요.

```bash
cd onprem-guide
pip install markdown pygments pyyaml pymdown-extensions
python3 build.py --check      # YAML·셸 블록 기계 검사 + dist/onprem-agent-deploy-guide.html 생성
```

- 실습 파일은 `lab/`에 있고, 부록 F는 빌드 시 `lab/`에서 자동으로 채워집니다. 실습 파일을 고치면 문서도 같이 바뀝니다.
- 상자 문법: `!!! why` / `expect` / `fail` / `eye` / `note` / `warn` / `tip` / `check` / `os` / `rollback` / `unverified` / `verified` / `say` / `checkpoint`.
- 화면 목업은 ```` ```screen ```` 블록(첫 줄 `# 제목`), 파일명 탭은 코드 블록 첫 줄 `#file: 경로`, 스크린샷은 `shots/`에 넣고 `![캡션](shots/x.png)`.
- 이미지 태그·도구 버전은 `00-intro.md`의 표와 `lab/bootstrap.sh`에 모여 있습니다. 태그가 사라지면 그 둘을 함께 고치세요.
