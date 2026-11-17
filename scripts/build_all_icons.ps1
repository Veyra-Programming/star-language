# =====================================================================
# Star Programming Language - Multi-Resolution Windows ICO Asset Builder
# Builds high-definition icons for:
# 1. .star source files (star_file.ico)
# 2. .starb bytecode files (star_bytecode.ico)
# 3. .starmobile mobile bundles (star_mobile.ico)
# 4. Star Compiler / Executable (star.ico)
# 5. WallpaperApp Nova3D (nova3d.ico)
# =====================================================================

Add-Type -AssemblyName System.Drawing

function Convert-PngToMultiResIco {
    param(
        [string]$InputPath,
        [string]$OutputPath,
        [int[]]$IconSizes = @(256, 128, 64, 48, 32, 24, 16)
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

    Write-Host "Generated: $OutputPath ($($frames.Count) frames: $($IconSizes -join ', ') px)"
    return $true
}

$assetsDir = "E:\Star Language\assets"
$srcFilePng = Join-Path $assetsDir "star_file_icon.png"

# 1. Ensure Bytecode PNG exists
$srcBmp = [System.Drawing.Bitmap]::FromFile($srcFilePng)
$bmpB = New-Object System.Drawing.Bitmap($srcBmp)
$gB = [System.Drawing.Graphics]::FromImage($bmpB)
$gB.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::HighQuality
$gB.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::AntiAliasGridFit

$rectB = New-Object System.Drawing.Rectangle(260, 765, 504, 130)
$b1 = [System.Drawing.Color]::FromArgb(255, 6, 78, 59)
$b2 = [System.Drawing.Color]::FromArgb(255, 16, 185, 129)
$brushB = New-Object System.Drawing.Drawing2D.LinearGradientBrush($rectB, $b1, $b2, [System.Drawing.Drawing2D.LinearGradientMode]::Horizontal)
$penB = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(255, 52, 211, 153), 4)

$pathB = New-Object System.Drawing.Drawing2D.GraphicsPath
$d = 40
$r = $rectB
$pathB.AddArc($r.X, $r.Y, $d, $d, 180, 90)
$pathB.AddArc($r.X + $r.Width - $d, $r.Y, $d, $d, 270, 90)
$pathB.AddArc($r.X + $r.Width - $d, $r.Y + $r.Height - $d, $d, $d, 0, 90)
$pathB.AddArc($r.X, $r.Y + $r.Height - $d, $d, $d, 90, 90)
$pathB.CloseFigure()

$gB.FillPath($brushB, $pathB)
$gB.DrawPath($penB, $pathB)

$dotBrushB = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(255, 251, 191, 36))
$gB.FillEllipse($dotBrushB, 310, 815, 24, 24)

$fontB = New-Object System.Drawing.Font("Segoe UI", 56, [System.Drawing.FontStyle]::Bold, [System.Drawing.GraphicsUnit]::Pixel)
$textBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::White)
$sf = New-Object System.Drawing.StringFormat
$sf.Alignment = [System.Drawing.StringAlignment]::Center
$sf.LineAlignment = [System.Drawing.StringAlignment]::Center
$gB.DrawString(".starb", $fontB, $textBrush, (New-Object System.Drawing.RectangleF(330, 765, 420, 130)), $sf)

$gB.Dispose()
$bytecodePng = Join-Path $assetsDir "star_bytecode_icon.png"
$bmpB.Save($bytecodePng, [System.Drawing.Imaging.ImageFormat]::Png)
$bmpB.Dispose()

# 2. Ensure Mobile PNG exists
$bmpM = New-Object System.Drawing.Bitmap($srcBmp)
$gM = [System.Drawing.Graphics]::FromImage($bmpM)
$gM.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::HighQuality
$gM.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::AntiAliasGridFit

$rectM = New-Object System.Drawing.Rectangle(200, 765, 624, 130)
$m1 = [System.Drawing.Color]::FromArgb(255, 112, 26, 117)
$m2 = [System.Drawing.Color]::FromArgb(255, 217, 70, 239)
$brushM = New-Object System.Drawing.Drawing2D.LinearGradientBrush($rectM, $m1, $m2, [System.Drawing.Drawing2D.LinearGradientMode]::Horizontal)
$penM = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(255, 244, 114, 182), 4)

$pathM = New-Object System.Drawing.Drawing2D.GraphicsPath
$rM = $rectM
$pathM.AddArc($rM.X, $rM.Y, $d, $d, 180, 90)
$pathM.AddArc($rM.X + $rM.Width - $d, $rM.Y, $d, $d, 270, 90)
$pathM.AddArc($rM.X + $rM.Width - $d, $rM.Y + $rM.Height - $d, $d, $d, 0, 90)
$pathM.AddArc($rM.X, $rM.Y + $rM.Height - $d, $d, $d, 90, 90)
$pathM.CloseFigure()

$gM.FillPath($brushM, $pathM)
$gM.DrawPath($penM, $pathM)

$dotBrushM = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(255, 56, 189, 248))
$gM.FillEllipse($dotBrushM, 240, 815, 24, 24)

$fontM = New-Object System.Drawing.Font("Segoe UI", 48, [System.Drawing.FontStyle]::Bold, [System.Drawing.GraphicsUnit]::Pixel)
$gM.DrawString(".starmobile", $fontM, $textBrush, (New-Object System.Drawing.RectangleF(260, 765, 550, 130)), $sf)

$gM.Dispose()
$mobilePng = Join-Path $assetsDir "star_mobile_icon.png"
$bmpM.Save($mobilePng, [System.Drawing.Imaging.ImageFormat]::Png)
$bmpM.Dispose()

$srcBmp.Dispose()

# 3. Generate All Multi-Resolution ICO files
Convert-PngToMultiResIco -InputPath $srcFilePng -OutputPath (Join-Path $assetsDir "star_file.ico")
Convert-PngToMultiResIco -InputPath $bytecodePng -OutputPath (Join-Path $assetsDir "star_bytecode.ico")
Convert-PngToMultiResIco -InputPath $mobilePng -OutputPath (Join-Path $assetsDir "star_mobile.ico")
Convert-PngToMultiResIco -InputPath (Join-Path $assetsDir "star_logo.png") -OutputPath (Join-Path $assetsDir "star.ico")
Convert-PngToMultiResIco -InputPath "E:\WallpaperApp\assets\logo\nova3d_app_icon.png" -OutputPath "E:\WallpaperApp\assets\logo\nova3d.ico"

# Also copy icons into a dedicated icons folder in assets
$iconsDir = Join-Path $assetsDir "icons"
if (-not (Test-Path $iconsDir)) {
    New-Item -ItemType Directory -Path $iconsDir -Force | Out-Null
}
Copy-Item (Join-Path $assetsDir "star_file.ico") (Join-Path $iconsDir "star_source.ico") -Force
Copy-Item (Join-Path $assetsDir "star_bytecode.ico") (Join-Path $iconsDir "star_bytecode.ico") -Force
Copy-Item (Join-Path $assetsDir "star_mobile.ico") (Join-Path $iconsDir "star_mobile.ico") -Force
Copy-Item (Join-Path $assetsDir "star.ico") (Join-Path $iconsDir "star.ico") -Force

Write-Host "`nAll Star Language Windows Icons built successfully!"

