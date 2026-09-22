{{- define "ax-agent.name" -}}{{ .Release.Name }}{{- end -}}
{{- define "ax-agent.labels" -}}
app: {{ include "ax-agent.name" . }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
helm.sh/chart: {{ .Chart.Name }}-{{ .Chart.Version }}
{{- end -}}
