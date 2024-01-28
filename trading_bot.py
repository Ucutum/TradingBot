import subprocess

# Пример выполнения команды "ls -l" в виде строки
command = "./TradingBot"
result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, text=True)

# Вывод результата
print(result.stdout)