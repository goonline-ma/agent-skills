# Render a .pptx with Microsoft PowerPoint COM (exact fidelity) and optionally export font-embedded .pptx + PDF.
# Usage:
#   powershell.exe -NoProfile -ExecutionPolicy Bypass -File render_deck_windows.ps1 -src "C:\abs\draft.pptx" [-outdir "C:\abs\render"] [-embedded "C:\abs\final.pptx"] [-pdf "C:\abs\final.pdf"]
param(
  [Parameter(Mandatory=$true)][string]$src,
  [string]$outdir = "",
  [string]$pdf = "",
  [string]$embedded = "",
  [int]$width = 1600,
  [int]$height = 900
)

$ErrorActionPreference = "Stop"
$srcAbs = (Resolve-Path -LiteralPath $src).Path
$wasRunning = @(Get-Process -Name "POWERPNT" -ErrorAction SilentlyContinue).Count -gt 0
$app = New-Object -ComObject PowerPoint.Application
$pres = $null

try {
  $pres = $app.Presentations.Open($srcAbs, $true, $false, $false)
  if ($outdir -ne "") {
    New-Item -ItemType Directory -Force -Path $outdir | Out-Null
    $i = 1
    foreach ($slide in $pres.Slides) {
      $target = Join-Path $outdir ("s{0:D2}.png" -f $i)
      $slide.Export($target, "PNG", $width, $height)
      $i++
    }
    Write-Output ("rendered_slides=" + ($i - 1))
  }
  if ($embedded -ne "") {
    $pres.SaveAs($embedded, 24, -1)  # ppSaveAsOpenXMLPresentation + msoTrue EmbedTrueTypeFonts
    Write-Output ("embedded_pptx=" + $embedded)
  }
  if ($pdf -ne "") {
    $pres.SaveAs($pdf, 32)           # ppSaveAsPDF
    Write-Output ("exported_pdf=" + $pdf)
  }
}
finally {
  if ($null -ne $pres) { $pres.Close() }
  if (-not $wasRunning -and $null -ne $app) { $app.Quit() }
}
