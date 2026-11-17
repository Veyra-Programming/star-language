# PowerShell Multi-Resolution Windows .ICO Generator for Star Programming Language
# Supports 256x256, 128x128, 64x64, 48x48, 32x32, 24x24, 16x16 with full 32-bit alpha transparency

param(
    [string]$SourcePng,
    [string]$TargetIco,
    [int[]]$Sizes = @(256, 128, 64, 48, 32, 24, 16)
)

Add-Type -AssemblyName System.Drawing

function Convert-PngToMultiResIco {
    param(
        [string]$InputPath,
        [string]$OutputPath,
        [int[]]$IconSizes
    )

    if (-not (Test-Path $InputPath)) {
        Write-Error "Source PNG not found: $InputPath"
        return $false
    }

    $srcBmp = [System.Drawing.Bitmap]::FromFile($InputPath)
    $frames = @()

    foreach ($size in $IconSizes) {
        $bmp = New-Object System.Drawing.Bitmap($size, $size, [System.Drawing.Imaging.PixelFormat]::Format32bppArgb)
        $g = [System.Drawing.Graphics]::FromImage($bmp)
        $g.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
        $g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::HighQuality
        $g.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality
        $g.CompositingQuality = [System.Drawing.Drawing2D.CompositingQuality]::HighQuality
        $g.Clear([System.Drawing.Color]::Transparent)
        $g.DrawImage($srcBmp, 0, 0, $size, $size)
        $g.Dispose()

        $ms = New-Object System.IO.MemoryStream
        $bmp.Save($ms, [System.Drawing.Imaging.ImageFormat]::Png)
        $bmp.Dispose()
        $pngBytes = $ms.ToArray()
        $ms.Dispose()

        $frames += [PSCustomObject]@{
            Size  = $size
            Bytes = $pngBytes
        }
    }
    $srcBmp.Dispose()

    $targetDir = [System.IO.Path]::GetDirectoryName($OutputPath)
    if (-not (Test-Path $targetDir)) {
        New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
    }

    $fs = [System.IO.File]::Create($OutputPath)
    $bw = New-Object System.IO.BinaryWriter($fs)

    # 1. ICONDIR Header (6 bytes)
    $bw.Write([uint16]0)                 # Reserved (0)
    $bw.Write([uint16]1)                 # Resource type: 1 = Icon
    $bw.Write([uint16]$frames.Count)     # Image count

    # 2. Directory Entries (16 bytes each)
    $dataOffset = 6 + ($frames.Count * 16)
    foreach ($f in $frames) {
        $w = if ($f.Size -ge 256) { [byte]0 } else { [byte]$f.Size }
        $h = if ($f.Size -ge 256) { [byte]0 } else { [byte]$f.Size }
        $bw.Write($w)                    # Width (0 = 256)
        $bw.Write($h)                    # Height (0 = 256)
        $bw.Write([byte]0)               # Color count (0 = >=8bpp)
        $bw.Write([byte]0)               # Reserved
        $bw.Write([uint16]1)             # Color planes
        $bw.Write([uint16]32)            # Bits per pixel
        $bw.Write([uint32]$f.Bytes.Length) # Image data size
        $bw.Write([uint32]$dataOffset)   # Offset of image data

        $dataOffset += $f.Bytes.Length
    }

    # 3. Image Data
    foreach ($f in $frames) {
        $bw.Write($f.Bytes)
    }

    $bw.Close()
    $fs.Close()

    Write-Host "Successfully generated: $OutputPath ($($frames.Count) frames: $($IconSizes -join ', ') px)"
    return $true
}

if ($SourcePng -and $TargetIco) {
    Convert-PngToMultiResIco -InputPath $SourcePng -OutputPath $TargetIco -IconSizes $Sizes
}

