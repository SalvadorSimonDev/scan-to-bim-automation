try {
    $data = $env:CLAUDE_TOOL_INPUT | ConvertFrom-Json
    $fp   = $data.file_path
    $name = Split-Path $fp -Leaf
    $ts   = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
    $log  = "$ts | WRITE | $name"

    $logPath = Join-Path $PSScriptRoot '..\build.log'
    Add-Content -Path $logPath -Value $log -Encoding UTF8 -ErrorAction SilentlyContinue
} catch {
    exit 0
}
