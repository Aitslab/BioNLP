## WSL2

docker info
docker-compose --version

Will confirm that our install can run docker wsl2 backend.  


Configure global options with .wslconfig

    Available in Windows Build 19041 and later

You can configure global WSL options by placing a .wslconfig file into the root directory of your users folder: C:\Users\<yourUserName>\.wslconfig. Many of these files are related to WSL 2, please keep in mind you may need to run wsl --shutdown to shut down the WSL 2 VM and then restart your WSL instance for these changes to take affect.

Here is a sample .wslconfig file:
Console

[wsl2]
kernel=C:\\temp\\myCustomKernel
memory=4GB # Limits VM memory in WSL 2 to 4 GB
processors=2 # Makes the WSL 2 VM use two virtual processors

This file can contain the following options:
WSL 2 Settings

## WSL condig
<h2 id="configure-global-options-with-wslconfig">Configure global options with .wslconfig</h2>
<blockquote>
<p><strong>Available in Windows Build 19041 and later</strong></p>
</blockquote>
<p>You can configure global WSL options by placing a <code>.wslconfig</code> file into the root directory of your users folder: <code>C:\Users\&lt;yourUserName&gt;\.wslconfig</code>. Many of these files are related to WSL 2, please keep in mind you may need to run <code>wsl --shutdown</code> to shut down the WSL 2 VM and then restart your WSL instance for these changes to take affect.</p>
<p>Here is a sample .wslconfig file:</p>
<pre><code class="lang-console">[wsl2]
kernel=C:\\temp\\myCustomKernel
memory=4GB # Limits VM memory in WSL 2 to 4 GB
processors=2 # Makes the WSL 2 VM use two virtual processors
</code></pre>
<p>This file can contain the following options:</p>
<h3 id="wsl-2-settings">WSL 2 Settings</h3>
<p>Section label: <code>[wsl2]</code></p>
<p>These settings affect the VM that powers any WSL 2 distribution.</p>
<table>
<thead>
<tr>
<th style="text-align: left;">key</th>
<th style="text-align: left;">value</th>
<th style="text-align: left;">default</th>
<th style="text-align: left;">notes</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: left;">kernel</td>
<td style="text-align: left;">string</td>
<td style="text-align: left;">The Microsoft built kernel provided inbox</td>
<td style="text-align: left;">An absolute Windows path to a custom Linux kernel.</td>
</tr>
<tr>
<td style="text-align: left;">memory</td>
<td style="text-align: left;">size</td>
<td style="text-align: left;">50% of total memory on Windows or 8GB, whichever is less; on builds before 20175: 80% of your total memory on Windows</td>
<td style="text-align: left;">How much memory to assign to the WSL 2 VM.</td>
</tr>
<tr>
<td style="text-align: left;">processors</td>
<td style="text-align: left;">number</td>
<td style="text-align: left;">The same number of processors on Windows</td>
<td style="text-align: left;">How many processors to assign to the WSL 2 VM.</td>
</tr>
<tr>
<td style="text-align: left;">localhostForwarding</td>
<td style="text-align: left;">boolean</td>
<td style="text-align: left;"><code>true</code></td>
<td style="text-align: left;">Boolean specifying if ports bound to wildcard or localhost in the WSL 2 VM should be connectable from the host via localhost:port.</td>
</tr>
<tr>
<td style="text-align: left;">kernelCommandLine</td>
<td style="text-align: left;">string</td>
<td style="text-align: left;">Blank</td>
<td style="text-align: left;">Additional kernel command line arguments.</td>
</tr>
<tr>
<td style="text-align: left;">swap</td>
<td style="text-align: left;">size</td>
<td style="text-align: left;">25% of memory size on Windows rounded up to the nearest GB</td>
<td style="text-align: left;">How much swap space to add to the WSL 2 VM, 0 for no swap file.</td>
</tr>
<tr>
<td style="text-align: left;">swapFile</td>
<td style="text-align: left;">string</td>
<td style="text-align: left;">%USERPROFILE%\AppData\Local\Temp\swap.vhdx</td>
<td style="text-align: left;">An absolute Windows path to the swap virtual hard disk.</td>
</tr>
</tbody>
</table>
<ul>
<li>Note: This value is true for Windows Build 19041 and may be different in Windows builds in the Insiders program</li>
</ul>
<p>Entries with the <code>path</code> value must be Windows paths with escaped backslashes, e.g: <code>C:\\Temp\\myCustomKernel</code></p>
<p>Entries with the <code>size</code> value must be a size followed by a unit, for example <code>8GB