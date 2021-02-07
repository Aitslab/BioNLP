## PROCESS SCOPE 

```
$env:testvariable = "Alpha"
```

```
$Env:windir
```

In this syntax, the dollar sign ($) indicates a variable, and the drive name (Env:) indicates an environment variable followed by the variable name (windir).

When you change environment variables in PowerShell, the change affects only the current session. This behavior resembles the behavior of the Set command in the Windows Command Shell and the Setenv command in UNIX-based environments. To change values in the Machine or User scopes, you must use the methods of the System.Environment class.


To set the environmental variable using PowerShell you need to use the assignment operator (=). If the variable already exists then you can use the += operator to append the value, otherwise, a new environment variable will be created.



## Using System.Environment methods

The System.Environment class provides GetEnvironmentVariable and SetEnvironmentVariable methods that allow you to specify the scope of the variable.

The following example uses the GetEnvironmentVariable method to get the machine setting of PSModulePath and the SetEnvironmentVariable method to add the C:\Program Files\Fabrikam\Modules path to the value.



```PowerShell
$path = [Environment]::GetEnvironmentVariable('PSModulePath', 'Machine')
$newpath = $path + ';C:\Program Files\Fabrikam\Modules'
[Environment]::SetEnvironmentVariable("PSModulePath", $newpath, 'Machine')
```

To set the environment persistently so they should remain even when close the session, PowerShell uses [System.Environment] class with the SetEnvironmentVariable method for the environment variable to set it persistently.

[System.Environment]::SetEnvironmentVariable('ResourceGroup','AZ_Resource_Group')


```
PS C:\> $env:ResourceGroup
AZ_Resource_Group
```

### Setting an Environment Variable with [System.Environment]

Use the SetEnvironmentVariable() method to set the value of an environment variable for the given scope, or create a new one if it does not already exist.

When setting variables in the process scope, you’ll find that the process scope is volatile while changes to the user and machine scopes are permanent.

```
PS51> [System.Environment]::SetEnvironmentVariable('TestVariable','Alpha','User')

PS51> [System.Environment]::SetEnvironmentVariable('TestVariable','Alpha','Process')

PS51> [System.Environment]::SetEnvironmentVariable('TestVariable','Alpha','Machine')

 # The same as Process
PS51> [System.Environment]::SetEnvironmentVariable('TestVariable','Alpha')
```

    Note: Calling the SetEnvironmentVariable method with a variable name or value of 32767 characters or more will cause an exception to be thrown.

Removing an Environment Variable with [System.Environment]

Use the SetEnvironmentVariable() method to remove an environment variable for the given scope by setting its value to an empty string.

```PowerShell
PS51> [System.Environment]::SetEnvironmentVariable('TestVariable', '', 'User')

PS51> [System.Environment]::SetEnvironmentVariable('TestVariable', '', 'Process')

PS51> [System.Environment]::SetEnvironmentVariable('TestVariable', '', 'Machine')

# The same as process
PS51> [System.Environment]::SetEnvironmentVariable('TestVariable', '')
```

