# 쿠버네티스 배포 (고객사에 OpenShift/K8s가 있는 경우)

    kubectl -n ax-pilot create secret generic agent-secret --from-literal=LLM_API_KEY='...' --from-literal=DB_DSN='...'
    kubectl apply -k .
    kubectl -n ax-pilot rollout status deployment/agent

- 이미지 주소·Ingress 클래스·호스트·NetworkPolicy의 ipBlock 은 고객사 값으로 교체한다.
- Helm 차트 형태가 필요하면 `../../day11/ax-agent/` 를 쓴다.
