Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;
using System.Text;

public class WinFG {
    [DllImport("user32.dll")]
    public static extern IntPtr GetForegroundWindow();

    [DllImport("user32.dll", CharSet = CharSet.Auto)]
    public static extern int GetWindowText(IntPtr hWnd, StringBuilder lpString, int nMaxCount);

    [DllImport("user32.dll")]
    public static extern uint GetWindowThreadProcessId(IntPtr hWnd, out uint lpdwProcessId);
}
"@

$hwnd = [WinFG]::GetForegroundWindow()
$p = 0
[WinFG]::GetWindowThreadProcessId($hwnd, [ref]$p)
$sb = New-Object System.Text.StringBuilder 256
[WinFG]::GetWindowText($hwnd, $sb, 256) | Out-Null
Write-Host "Foreground HWND: $hwnd | PID: $p | Title: $($sb.ToString())"
