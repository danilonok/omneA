# Define paths to search (Program Files, Start Menu, etc.)
$searchPaths = @(
    "$env:ProgramFiles",
    "$env:ProgramFiles(x86)",
    "$env:ProgramData\Microsoft\Windows\Start Menu\Programs",
    "$env:AppData\Microsoft\Windows\Start Menu\Programs"
)

# Create an array to hold results
$results = @()

# Search for .lnk (shortcut) files that likely point to .exe files
foreach ($path in $searchPaths) {
    if (Test-Path $path) {
        Get-ChildItem -Path $path -Recurse -Filter *.lnk -ErrorAction SilentlyContinue | ForEach-Object {
            try {
                $shell = New-Object -ComObject WScript.Shell
                $shortcut = $shell.CreateShortcut($_.FullName)
                if ($shortcut.TargetPath -and ($shortcut.TargetPath -like "*.exe")) {
                    $results += [PSCustomObject]@{
                        Name = $_.BaseName
                        Path = $shortcut.TargetPath
                    }
                }
            } catch {}
        }
    }
}

# Remove duplicates and sort
$results = $results | Sort-Object Name -Unique

# Output to console
$results | Format-Table -AutoSize

# Optional: Export to CSV
$results | Export-Csv -Path "$env:USERPROFILE\Desktop\InstalledApps.csv" -NoTypeInformation -Encoding UTF8
