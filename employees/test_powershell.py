from employees.start_maintenance_action import StartMaintenanceAction


class TestPowerShell(StartMaintenanceAction):
    def proceed(self)->str:
        import subprocess

        command:str='Get-Process'

        try:
            output = subprocess.run(['powershell', '-Command', command], capture_output=True, text=True)
        except FileNotFoundError:
            output = subprocess.run(['pwsh', '-Command', command], capture_output=True, text=True)

        print(output.stdout)

        return output.stdout