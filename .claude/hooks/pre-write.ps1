try {
    $data = $env:CLAUDE_TOOL_INPUT | ConvertFrom-Json
    $fp   = $data.file_path
    $ct   = $data.content

    if ($fp -match '\.py$' -and $ct -match 'Transaction' -and $ct -notmatch 'RollBack') {
        Write-Output '[BIM-GUARD] Transaction sin RollBack detectada. El script puede corromper el modelo si falla. Añade RollBack en el bloque except.'
        exit 2
    }
} catch {
    exit 0
}
