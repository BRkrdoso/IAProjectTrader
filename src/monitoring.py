import psutil
import time
import cProfile
import pstats
from io import StringIO

# Função para monitorar uso de CPU e Memória
def monitor_resources():
    cpu_percent = psutil.cpu_percent(interval=1)
    memory_info = psutil.virtual_memory()
    memory_percent = memory_info.percent
    return cpu_percent, memory_percent

# Função para monitorar o tempo de execução de uma função específica
def profile_function(func, *args, **kwargs):
    profiler = cProfile.Profile()
    profiler.enable()
    start_time = time.time()
    
    result = func(*args, **kwargs)  # Executa a função monitorada
    
    end_time = time.time()
    profiler.disable()
    
    # Calcula o tempo de execução
    execution_time = end_time - start_time
    
    # Gera o relatório de perfil
    profiler_stats = StringIO()
    ps = pstats.Stats(profiler, stream=profiler_stats).sort_stats('cumulative')
    ps.print_stats()
    
    return result, execution_time, profiler_stats.getvalue()

# Exemplo de função a ser monitorada
def example_function():
    time.sleep(2)  # Simula uma operação que leva tempo
    return "Função executada"

# Função principal para monitorar gargalos
def monitor_system():
    cpu_limit = 80  # Limite de CPU para detecção de gargalo (%)
    memory_limit = 70  # Limite de uso de memória para detecção de gargalo (%)
    time_limit = 1.5  # Limite de tempo de execução (segundos)
    
    # Monitoramento de recursos
    cpu_usage, memory_usage = monitor_resources()
    
    if cpu_usage > cpu_limit:
        print(f"Gargalo detectado: Uso de CPU alto - {cpu_usage}%")
    
    if memory_usage > memory_limit:
        print(f"Gargalo detectado: Uso de Memória alto - {memory_usage}%")
    
    # Monitoramento de tempo de execução
    result, exec_time, profile_data = profile_function(example_function)
    
    if exec_time > time_limit:
        print(f"Gargalo detectado: Função demorou muito - {exec_time} segundos")
    
    # Exibe os resultados do monitoramento
    print(f"Resultado da função: {result}")
    print(f"Tempo de execução: {exec_time} segundos")
    print("Perfil da função:")
    print(profile_data)

# Executa o monitoramento
if __name__ == "__main__":
    monitor_system()
