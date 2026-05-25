try {
    $data = $env:CLAUDE_TOOL_INPUT | ConvertFrom-Json
    $cmd  = $data.command

    $destructivo = $cmd -match 'rm\s+-rf|Remove-Item.*-Recurse.*-Force|drop\s+table|DELETE\s+FROM'
    $seguro      = $cmd -match 'node_modules|__pycache__|\.pyc'

    if ($destructivo -and -not $seguro) {
        Write-Output '[BIM-GUARD] Comando destructivo detectado. Confirma antes de continuar.'
        exit 2
    }
} catch {
    exit 0
}
