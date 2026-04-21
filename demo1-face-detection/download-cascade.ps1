# PowerShell script to download the Haar Cascade file

$url = "https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml"
$output = "haarcascade_frontalface_default.xml"

Write-Host "Downloading Haar Cascade classifier for face detection..."
Write-Host "From: $url"
Write-Host "To: $output"
Write-Host ""

try {
    Invoke-WebRequest -Uri $url -OutFile $output
    Write-Host "Download completed successfully!" -ForegroundColor Green
    Write-Host "File saved to: $output"
    
    # Verify file size
    $fileSize = (Get-Item $output).Length
    Write-Host "File size: $($fileSize / 1KB) KB"
    
    if ($fileSize -lt 1000) {
        Write-Host "Warning: File seems too small. Download may have failed." -ForegroundColor Yellow
    }
}
catch {
    Write-Host "Error downloading file: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "Alternative: Download manually from:"
    Write-Host $url
    exit 1
}
