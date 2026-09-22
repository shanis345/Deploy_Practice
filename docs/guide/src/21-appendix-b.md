# 부록 B — 명령어 치트시트

현장에서 자주 쓰는 순서대로. `<>` 안은 바꿔 넣는 값입니다.

## B-1. Docker

```bash
# 이미지
docker build -t <이미지>:<태그> .
docker build --network=none -f Dockerfile.offline -t x:1 .   # 폐쇄망 빌드 검증
docker build --build-arg HTTPS_PROXY=http://<프록시>:3128 ...  # 빌드 시 프록시
docker build --build-arg BASE=python:3.12.14-slim ...           # 베이스 태그 교체
docker images
docker history <이미지>                                         # 레이어별 크기
docker image inspect <이미지> --format '{{.Config.User}} {{index .RepoDigests 0}}'
docker save <이미지> -o out.tar && gzip -9 -k out.tar           # 반입용
docker load -i out.tar                                          # 반입 후
docker tag <이미지> harbor.corp.local/<프로젝트>/<이미지>:<태그> && docker push ...
docker system df && docker image prune -f                       # 디스크 정리

# 컨테이너
docker run -d --name x -p 127.0.0.1:8000:8000 <이미지>
docker run --rm --read-only --tmpfs /app/tmp <이미지> ...        # 읽기 전용 검증
docker exec -it x sh
docker exec x id                                                # non-root 확인
docker logs -f --tail 100 x
docker stats --no-stream
docker inspect x --format '{{.State.Health.Status}} {{.RestartCount}}'
docker rm -f x

# 네트워크
docker network create <net>
docker network create --internal <net>                          # 인터넷 차단
docker network inspect <net> --format '{{range .Containers}}{{.Name}} {{.IPv4Address}}{{"\n"}}{{end}}'
docker network connect <net> <컨테이너>
docker inspect <컨테이너> --format '{{json .NetworkSettings.Networks}}' | jq
docker port <컨테이너>

# 취약점·SBOM (trivy 컨테이너)
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock -v "$PWD/trivy-cache:/root/.cache/" \
  aquasec/trivy:0.56.2 image --severity HIGH,CRITICAL --scanners vuln <이미지>
  # 폐쇄망: --skip-db-update --skip-java-db-update, --ignore-unfixed (패치 있는 것만)
  # SBOM: --format cyclonedx --output sbom.json
```

## B-2. Docker Compose

```bash
docker compose config --quiet            # 문법·치환 확인 (올리기 전에 항상)
docker compose config | grep -A3 <서비스>  # 최종 설정 (변수 치환 결과)
docker compose up -d
docker compose up -d --force-recreate <서비스>   # .env 변경 반영
docker compose ps
docker compose logs -f --tail 100 <서비스>
docker compose exec <서비스> sh
docker compose exec -T <서비스> <명령>     # 스크립트 안에서
docker compose restart <서비스>          # 환경변수는 다시 안 읽음
docker compose stop/start <서비스>
docker compose down                      # 볼륨 유지
docker compose down -v                   # 볼륨까지 삭제
```

## B-3. 리눅스 네트워크

```bash
ip -brief addr                           # 인터페이스와 IP
ip route                                 # 라우팅 (default가 있는가)
ip netns list; sudo ip netns exec <ns> <명령>
bridge link                              # 브리지 포트
sudo ss -ltnp                            # 리슨 중인 포트와 프로세스 (127.0.0.1 vs 0.0.0.0)
sudo iptables -t nat -S POSTROUTING      # NAT 규칙
sudo iptables -S FORWARD | head
sudo tcpdump -ni <if> -c 20 tcp port <포트>   # [S]만 있고 [S.]가 없으면 서버 미응답
sudo nsenter -t $(docker inspect <컨테이너> --format '{{.State.Pid}}') -n ip addr   # 컨테이너 netns 들여다보기
```

## B-4. 진단 3단계 (외우세요)

```bash
# ① 이름이 풀리는가            실패 → DNS / 네트워크 소속 / NetworkPolicy DNS 규칙
nslookup <호스트>
dig +short <호스트>
getent hosts <호스트>

# ② 포트가 열려 있는가          refused → 서비스 미기동·127.0.0.1 바인딩 / timeout → 방화벽·라우팅
nc -zv -w3 <호스트> <포트>
timeout 3 bash -c "</dev/tcp/<호스트>/<포트>" && echo OPEN || echo CLOSED   # nc가 없을 때

# ③ 애플리케이션이 응답하는가   실패 → 인증·경로·TLS·타임아웃
curl -sv -m5 http://<호스트>:<포트>/healthz -o /dev/null 2>&1 | grep -E "^< HTTP|Connected"
curl -s -o /dev/null -w '%{http_code} %{time_total}s\n' <url>

# 프록시 경유 확인
curl -sv -x http://<프록시>:3128 https://<목적지> -o /dev/null 2>&1 | grep -E "CONNECT|HTTP/"
# 인증서 확인 (프록시 경유)
openssl s_client -connect <호스트>:443 -servername <호스트> -proxy <프록시>:3128 </dev/null 2>/dev/null | grep -E "issuer=|subject=|Verify"
# 번들에 사내 CA가 있는가
grep -c "BEGIN CERTIFICATE" /etc/ssl/certs/ca-certificates.crt
```

## B-5. kubectl

```bash
# 컨텍스트·권한
kubectl config get-contexts; kubectl config use-context <ctx>
kubectl auth can-i --list -n <ns>
kubectl get ingressclass; kubectl get pods -n kube-system | grep -Ei "calico|cilium|flannel|ovn|antrea"

# 조회
kubectl -n <ns> get pods -o wide
kubectl -n <ns> get all
kubectl -n <ns> get events --sort-by=.lastTimestamp | tail -20
kubectl get ns --show-labels

# 진단 (이 순서로)
kubectl -n <ns> describe pod <pod> | grep -A15 "^Events"
kubectl -n <ns> logs <pod>
kubectl -n <ns> logs <pod> --previous              # CrashLoop
kubectl -n <ns> exec -it <pod> -- sh
kubectl -n <ns> run netshoot --rm -it --image=nicolaka/netshoot:v0.13 --restart=Never -- sh
kubectl -n <ns> port-forward svc/<svc> 8000:8000   # 진단용. 부하 분산 안 됨

# 배포
kubectl apply -f <파일|디렉터리>  /  kubectl apply -k <kustomize 디렉터리>
kubectl -n <ns> rollout status deployment/<name>
kubectl -n <ns> rollout restart deployment/<name>  # 무중단 재시작 (환경변수 반영)
kubectl -n <ns> rollout history deployment/<name>
kubectl -n <ns> rollout undo deployment/<name>     # 롤백
kubectl -n <ns> set image deployment/<name> <컨테이너>=<이미지>
kubectl -n <ns> scale deployment/<name> --replicas=3

# 설정·비밀
kubectl -n <ns> create configmap <name> --from-file=prompt.txt
kubectl -n <ns> patch configmap <name> --type merge -p '{"data":{"KEY":"value"}}'
kubectl -n <ns> create secret generic <name> --from-literal=KEY=value
kubectl -n <ns> create secret docker-registry harbor-cred --docker-server=harbor.corp.local --docker-username=<u> --docker-password=<p>
kubectl -n <ns> get secret <name> -o jsonpath='{.data.KEY}' | base64 -d

# 노드 (권한이 있을 때)
kubectl get nodes -o wide
kubectl drain <node> --ignore-daemonsets --delete-emptydir-data; kubectl uncordon <node>
kubectl top pods -n <ns>                           # metrics-server 필요
```

## B-6. Helm

```bash
helm lint <차트>
helm template <릴리스> <차트> -f values-<env>.yaml -n <ns>     # 렌더링만
helm install <릴리스> <차트> -f values-<env>.yaml -n <ns> --wait
helm upgrade <릴리스> <차트> -f values-<env>.yaml -n <ns> --set key=value --wait
helm -n <ns> list; helm -n <ns> history <릴리스>
helm -n <ns> rollback <릴리스> <revision>
helm -n <ns> uninstall <릴리스>
```

## B-7. 자주 쓰는 진단 이미지

| 이미지 | 용도 | 크기 |
|---|---|---|
| `nicolaka/netshoot:v0.13` | dig, curl, nc, tcpdump, netstat, iperf 전부 | 775MB |
| `curlimages/curl` | 최소 curl | 20MB |
| `alpine/openssl` | 인증서 확인 | 10MB |
| `postgres:16.4-alpine` | psql 클라이언트 | 359MB |
| `traefik/whoami:v1.10` | 요청 헤더·호스트 에코 | 11MB |

**폐쇄망 반입 목록에 최소 `nicolaka/netshoot`은 꼭 포함하세요.**

## B-8. TUI 도구 단축키

| 도구 | 키 | 동작 |
|---|---|---|
| lazydocker | `[` `]` | 오른쪽 탭 (Logs / Stats / Env / Config) |
| | `d` | 삭제 (컨테이너·이미지) |
| | `x` | 메뉴 |
| k9s | `:pods` `:deploy` `:svc` `:cm` `:secrets` `:ing` `:netpol` `:events` `:helm` | 리소스 뷰 |
| | `/` | 필터 |
| | `d` `l` `p` `s` `y` | describe / 로그 / 이전 로그 / 셸 / YAML |
| | `x` | (secrets) 디코드 |
| | `Ctrl`+`d` | 삭제 |
| dive | `Tab` | 레이어 ↔ 파일 트리 |
| | `Ctrl`+`L` | 해당 레이어의 변경만 |
| | `Ctrl`+`F` | 파일 필터 |
