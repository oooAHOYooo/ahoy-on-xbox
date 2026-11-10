# Run only on the disposable Windows screenshot runner. Never publishes or uploads a Store submission.
$ErrorActionPreference = 'Stop'
$out = Join-Path $PWD 'dist/native-captures'
New-Item -ItemType Directory -Force -Path $out | Out-Null
Start-Transcript -Path (Join-Path $out 'capture-log.txt')
try {
  Get-ComputerInfo -Property WindowsProductName, WindowsVersion, OsBuildNumber | Format-List
  $bundle = Get-ChildItem AhoyXbox/CapturePackages -Recurse -Include *.msixbundle,*.appxbundle | Select-Object -First 1
  if (-not $bundle) { throw 'No signed test bundle was generated.' }
  Get-ChildItem $bundle.Directory.FullName -Recurse -Filter *.appx | Where-Object { $_.FullName -match 'Dependencies\\x64' } | ForEach-Object {
    Add-AppxPackage -Path $_.FullName
  }
  Add-AppxPackage -Path $bundle.FullName
  $package = Get-AppxPackage -Name AhoyIndieMedia.AHOYTV
  if (-not $package) { throw 'Native test package is not installed.' }
  Add-Type -AssemblyName UIAutomationClient, UIAutomationTypes, System.Drawing
  Add-Type @'
using System;
using System.Runtime.InteropServices;
[ComImport, Guid("45BA127D-10A8-46EA-8AB7-56EA9078943C")] class AhoyActivationManager {}
[ComImport, Guid("2E941141-7F97-4756-BA1D-9DECDE894A3D"), InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
interface IAhoyActivationManager {
 [PreserveSig] int ActivateApplication([MarshalAs(UnmanagedType.LPWStr)] string app, [MarshalAs(UnmanagedType.LPWStr)] string args, uint options, out uint process);
}
public static class AhoyNativeLaunch {
 public static uint Launch(string app) {
   uint process;
   int hr = ((IAhoyActivationManager)new AhoyActivationManager()).ActivateApplication(app, "", 0, out process);
   Marshal.ThrowExceptionForHR(hr);
   return process;
 }
 [DllImport("user32.dll")] public static extern bool SetProcessDPIAware();
 [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr window);
 [DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow();
}
'@
  [AhoyNativeLaunch]::SetProcessDPIAware() | Out-Null
  $appProcess = [AhoyNativeLaunch]::Launch("$($package.PackageFamilyName)!App")
  Write-Host "Activated native app process $appProcess"
  Start-Sleep -Seconds 20
  $condition = New-Object System.Windows.Automation.PropertyCondition([System.Windows.Automation.AutomationElement]::NameProperty, 'AHOY TV')
  $window = [System.Windows.Automation.AutomationElement]::RootElement.FindFirst([System.Windows.Automation.TreeScope]::Children, $condition)
  if (-not $window) { throw 'No native AHOY TV window is visible on the runner desktop.' }
  $window.GetCurrentPattern([System.Windows.Automation.WindowPattern]::Pattern).SetWindowVisualState([System.Windows.Automation.WindowVisualState]::Maximized)
  [AhoyNativeLaunch]::SetForegroundWindow([IntPtr]$window.Current.NativeWindowHandle) | Out-Null
  $scenes = @(@('LIVE TV','01-Live-TV'), @('ON DEMAND','02-On-Demand'), @('MUSIC','03-Music'), @('RADIO','04-Radio'))
  foreach ($scene in $scenes) {
    $buttonCondition = New-Object System.Windows.Automation.PropertyCondition([System.Windows.Automation.AutomationElement]::NameProperty, $scene[0])
    $button = $window.FindFirst([System.Windows.Automation.TreeScope]::Descendants, $buttonCondition)
    if (-not $button) { throw "Native section button missing: $($scene[0])" }
    $button.GetCurrentPattern([System.Windows.Automation.InvokePattern]::Pattern).Invoke()
    Start-Sleep -Seconds 5
    $window.SetFocus()
    $rect = $window.Current.BoundingRectangle
    if ($rect.Width -lt 1280 -or $rect.Height -lt 720) { throw "Runner desktop is too small: $rect" }
    if ([AhoyNativeLaunch]::GetForegroundWindow() -ne [IntPtr]$window.Current.NativeWindowHandle) { throw 'The app is not foreground; refusing desktop capture.' }
    $image = New-Object System.Drawing.Bitmap ([int]$rect.Width), ([int]$rect.Height)
    $graphics = [System.Drawing.Graphics]::FromImage($image)
    try {
      $graphics.CopyFromScreen([int]$rect.X, [int]$rect.Y, 0, 0, $image.Size)
      $image.Save((Join-Path $out "$($scene[1]).png"), [System.Drawing.Imaging.ImageFormat]::Png)
    } finally { $graphics.Dispose(); $image.Dispose() }
    $nodes = $window.FindAll([System.Windows.Automation.TreeScope]::Descendants, [System.Windows.Automation.Condition]::TrueCondition)
    $nodes | ForEach-Object { $_.Current.Name } | Set-Content (Join-Path $out "$($scene[1])-ui.txt")
  }
} finally { Stop-Transcript }
