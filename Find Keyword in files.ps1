# Specify the directory to search for files
$directory = "."

# Define the keyword to match
$keyword = "keyword"

# Define the number of lines to show before and after the matched keyword
$contextLines = 3

# Recursively search for files and match the keyword
Get-ChildItem $directory -Recurse | Where-Object {$_.PSIsContainer -eq $false} | ForEach-Object {
    $fileContent = Get-Content $_.FullName
    $fileContent | Select-String -Pattern $keyword -Context $contextLines | ForEach-Object {
        Write-Host "Match found in file: $($_.Filename)"
        Write-Host "Context: $_.Context.PreContext"
        Write-Host "         $_.Line"
        Write-Host "         $_.Context.PostContext"
        Write-Host ""
    }
}
