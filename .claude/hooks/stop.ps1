try {
    $ts       = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
    $logPath  = Join-Path $PSScriptRoot '..\build.log'

    Add-Content -Path $logPath -Value "$ts | SESSION END" -Encoding UTF8 -ErrorAction SilentlyContinue

    $count = 0
    if (Test-Path $logPath) {
        $count = (Get-Content $logPath | Where-Object { $_ -match 'WRITE.*\.py' }).Count
    }

    if ($count -gt 0) {
        Write-Output "[BIM Agent] Sesion cerrada. $count script(s) Python generados. Registra los cambios en git."
    }
} catch {
    exit 0
}
