$url = "https://shop.flipperzero.one"
$url2 = "https://lab401.com/products/flipper-zero?variant=42927883485414"
$interval = 30

while ($true) {
    # Retrieve the webpage HTML
    $html = (Invoke-WebRequest -Uri $url).Content
    $html2 = (Invoke-WebRequest -Uri $url2).Content

    # Check if the HTML contains the words "sold out"
    if ($html -notmatch "sold out") {
        # Display a notification if the words "sold out" are not found
        [Windows.Forms.MessageBox]::Show("FlipperZero.one - BUY FLIPPER ZERO NOW!!!", "Notification")
        (New-Object Media.SoundPlayer "C:\Users\David\Desktop\alarm.wav").PlaySync()
        Write-Host "FlipperZero Shop - IN STOCK"
    }
    else {
        Write-Host "FlipperZero Shop - SOLD OUT"
    }

        # Check if the HTML contains the words "sold out"
    if ($html2 -notmatch "Sold Out") {
        # Display a notification if the words "sold out" are not found
        [Windows.Forms.MessageBox]::Show("LAB401 - BUY FLIPPER ZERO NOW!!!", "Notification")
        (New-Object Media.SoundPlayer "C:\Users\David\Desktop\alarm.wav").PlaySync()
        Write-Host "LAB401 - IN STOCK"

    }
    else {
        Write-Host "LAB401 - SOLD OUT"
    }
    # Wait for the specified interval before checking again
    Start-Sleep -Seconds $interval
}