# 🧼 Remove UTF-8 BOM from all files in a folder (recursively)
param (
    [string]$folderPath = ".",
    [string]$filePattern = "*.cl"
)

# Convert path to full format
$fullPath = Resolve-Path $folderPath

# Get all matching files
$files = Get-ChildItem -Path $fullPath -Recurse -File -Filter $filePattern

foreach ($file in $files) {
    $bytes = [System.IO.File]::ReadAllBytes($file.FullName)

    # Detect BOM: EF BB BF
    if ($bytes.Length -ge 3 -and $bytes[0] -eq 0xEF -and $bytes[1] -eq 0xBB -and $bytes[2] -eq 0xBF) {
        Write-Host "🚫 BOM found in $($file.FullName). Stripping..."
        $cleanBytes = $bytes[3..($bytes.Length - 1)]
        [System.IO.File]::WriteAllBytes($file.FullName, $cleanBytes)
    } else {
        Write-Host "✅ No BOM in $($file.FullName)"
    }
}