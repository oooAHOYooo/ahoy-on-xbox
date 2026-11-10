param([string]$OutputDirectory = "$PSScriptRoot\..\dist\release\screenshots")
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Drawing
Add-Type @'
using System;
using System.Text;
using System.Runtime.InteropServices;
public static class AhoyWindowCapture {
  [StructLayout(LayoutKind.Sequential)] public struct RECT { public int Left, Top, Right, Bottom; }
  [StructLayout(LayoutKind.Sequential)] public struct POINT { public int X, Y; }
  [DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow();
  [DllImport("user32.dll")] public static extern bool GetClientRect(IntPtr h, out RECT r);
  [DllImport("user32.dll")] public static extern bool ClientToScreen(IntPtr h, ref POINT p);
  [DllImport("user32.dll", CharSet=CharSet.Unicode)] public static extern int GetWindowText(IntPtr h, StringBuilder s, int n);
  [DllImport("user32.dll")] public static extern bool SetProcessDPIAware();
}
'@
[AhoyWindowCapture]::SetProcessDPIAware() | Out-Null
New-Item -ItemType Directory -Force -Path $OutputDirectory | Out-Null
Write-Host 'Run the native AHOY TV app, maximize it, and wait for images to load.'
Write-Host 'For each scene, press Enter here, then switch to AHOY TV within 5 seconds.'
Write-Host 'Only the foreground AHOY window is captured. Browser preview windows are rejected.'
$scenes = @('01-Live-TV', '02-On-Demand', '03-Music', '04-Radio')
foreach ($scene in $scenes) {
  Read-Host "Open $scene in the native app; press Enter when ready" | Out-Null
  Start-Sleep -Seconds 5
  $window = [AhoyWindowCapture]::GetForegroundWindow()
  $title = New-Object System.Text.StringBuilder 512
  [AhoyWindowCapture]::GetWindowText($window, $title, 512) | Out-Null
  if ($title.ToString() -notmatch '^AHOY TV$') {
    throw "Foreground window is '$title', not the native AHOY TV window. No image saved."
  }
  $bounds = New-Object AhoyWindowCapture+RECT
  $origin = New-Object AhoyWindowCapture+POINT
  if (-not [AhoyWindowCapture]::GetClientRect($window, [ref]$bounds)) { throw 'Cannot read app bounds.' }
  [AhoyWindowCapture]::ClientToScreen($window, [ref]$origin) | Out-Null
  $width = $bounds.Right - $bounds.Left
  $height = $bounds.Bottom - $bounds.Top
  if ($width -lt 1280 -or $height -lt 720) { throw 'App is too small. Maximize it on a 1080p or higher display.' }
  $bitmap = New-Object System.Drawing.Bitmap $width, $height
  $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
  try {
    $graphics.CopyFromScreen($origin.X, $origin.Y, 0, 0, $bitmap.Size)
    $file = Join-Path $OutputDirectory "$scene.png"
    $bitmap.Save($file, [System.Drawing.Imaging.ImageFormat]::Png)
    Write-Host "Saved $file (${width}x${height}); review that the correct scene is visible."
  } finally { $graphics.Dispose(); $bitmap.Dispose() }
}
Write-Host 'Review all images before uploading. These are actual window captures, without resizing or added artwork.'
