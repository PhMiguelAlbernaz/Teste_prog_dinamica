import collections


# Define a função que queremos integrar (exemplo: f(x) = x^2)
def funcao_para_integrar(valor_x):
    # Contabiliza a avaliação da função
    funcao_para_integrar.contador_avaliacoes += 1
    return valor_x ** 2


# Inicializa o contador de avaliações da função
funcao_para_integrar.contador_avaliacoes = 0


def integrar_adaptativo(func_integral, limite_inferior, limite_superior, precisao_total):
    """
    Algoritmo de integração numérica adaptativa (abordagem dinâmica).

    Args:
        func_integral: A função a ser integrada (f(x)).
        limite_inferior: Limite inferior do intervalo.
        limite_superior: Limite superior do intervalo.
        precisao_total: Tolerância de erro total desejada.

    Returns:
        O valor aproximado da integral.
    """
    func_integral.contador_avaliacoes = 0  # Reinicia o contador para cada execução da integral

    # Usamos uma pilha para gerenciar os subintervalos a serem processados.
    # Cada item na pilha será uma tupla: (inicio_intervalo, fim_intervalo, nivel_subdivisao, valor_f_inicio, valor_f_fim)
    # valor_f_inicio e valor_f_fim são os valores de func_integral(inicio_intervalo) e func_integral(fim_intervalo)
    # para evitar reavaliações.

    # Avalia os pontos iniciais e adiciona o intervalo completo à pilha
    valor_f_inicio_total = func_integral(limite_inferior)
    valor_f_fim_total = func_integral(limite_superior)

    pilha_subintervalos = collections.deque(
        [(limite_inferior, limite_superior, 0, valor_f_inicio_total, valor_f_fim_total)])

    resultado_integral_acumulado = 0.0

    while pilha_subintervalos:
        intervalo_atual_inicio, intervalo_atual_fim, nivel_atual, f_val_inicio_atual, f_val_fim_atual = pilha_subintervalos.pop()

        largura_intervalo = intervalo_atual_fim - intervalo_atual_inicio
        ponto_medio_intervalo = (intervalo_atual_inicio + intervalo_atual_fim) / 2.0

        # Avalia a função no ponto médio (esta é a única nova avaliação por iteração)
        valor_f_ponto_medio = func_integral(ponto_medio_intervalo)

        # 1. Calcular Regra do Trapézio para o intervalo atual
        # Reutiliza f_val_inicio_atual e f_val_fim_atual
        regra_trapezio = (largura_intervalo / 2.0) * (f_val_inicio_atual + f_val_fim_atual)

        # 2. Calcular Regra de Simpson para o intervalo atual
        # Reutiliza f_val_inicio_atual, f_val_fim_atual e usa valor_f_ponto_medio
        regra_simpson = (largura_intervalo / 6.0) * (f_val_inicio_atual + 4 * valor_f_ponto_medio + f_val_fim_atual)

        # 3. Estimar o erro para este intervalo
        estimativa_erro = abs(regra_trapezio - regra_simpson)

        # Critério de subdivisão: |T - S| > precisao_total / 2^(nivel_atual + 1)
        tolerancia_para_este_intervalo = precisao_total / (2 ** (nivel_atual + 1))

        if estimativa_erro > tolerancia_para_este_intervalo:
            # Subdividir o intervalo: adicionar dois novos subintervalos à pilha

            # Subintervalo esquerdo: [intervalo_atual_inicio, ponto_medio_intervalo]
            # f(intervalo_atual_inicio) é f_val_inicio_atual (reutilizado)
            # f(ponto_medio_intervalo) é valor_f_ponto_medio (reutilizado)
            pilha_subintervalos.append(
                (intervalo_atual_inicio, ponto_medio_intervalo, nivel_atual + 1, f_val_inicio_atual,
                 valor_f_ponto_medio))

            # Subintervalo direito: [ponto_medio_intervalo, intervalo_atual_fim]
            # f(ponto_medio_intervalo) é valor_f_ponto_medio (reutilizado)
            # f(intervalo_atual_fim) é f_val_fim_atual (reutilizado)
            pilha_subintervalos.append(
                (ponto_medio_intervalo, intervalo_atual_fim, nivel_atual + 1, valor_f_ponto_medio, f_val_fim_atual))
        else:
            # O intervalo é "bom o suficiente", adicionamos a aproximação de Simpson à integral total
            resultado_integral_acumulado += regra_simpson

    return resultado_integral_acumulado


# --- Teste do Algoritmo ---
print("--- Teste com a função f(x) = x^2 ---")

# Integral de x^2 de 0 a 1 é x^3/3 de 0 a 1 = 1/3 = 0.333333...
inicio_teste = 0.0
fim_teste = 1.0
epsilon_teste = 1e-6  # Tolerância de erro

print(f"\nCalculando a integral de f(x) = x^2 de {inicio_teste} a {fim_teste} com precisão = {epsilon_teste}")
resultado_obtido = integrar_adaptativo(funcao_para_integrar, inicio_teste, fim_teste, epsilon_teste)

print(f"Resultado da Integral: {resultado_obtido}")
print(f"Número de avaliações da função f: {funcao_para_integrar.contador_avaliacoes}")
print(f"Valor real (para x^2 de 0 a 1): {1 / 3}")

# --- Outro Exemplo: f(x) = sin(x) ---
import math


def outra_funcao(val):
    outra_funcao.contador_avaliacoes += 1
    return math.sin(val)


outra_funcao.contador_avaliacoes = 0  # Reinicia o contador

# Integral de sen(x) de 0 a pi é -cos(x) de 0 a pi = (-(-1)) - (-1) = 1 + 1 = 2
inicio_outra = 0.0
fim_outra = math.pi
epsilon_outra = 1e-7  # Tolerância de erro mais apertada

print(f"\n--- Teste com a função f(x) = sin(x) ---")
print(f"\nCalculando a integral de f(x) = sin(x) de {inicio_outra} a {fim_outra} com precisão = {epsilon_outra}")
resultado_outra = integrar_adaptativo(outra_funcao, inicio_outra, fim_outra, epsilon_outra)

print(f"Resultado da Integral: {resultado_outra}")
print(f"Número de avaliações da função f: {outra_funcao.contador_avaliacoes}")
print(f"Valor real (para sin(x) de 0 a pi): {2.0}")


# --- Exemplo com função mais "difícil" (para ver mais subdivisões) ---
def funcao_dificil(val):
    funcao_dificil.contador_avaliacoes += 1
    return math.sqrt(val)


funcao_dificil.contador_avaliacoes = 0  # Reinicia o contador

# Integral de sqrt(x) de 0 a 1 é (2/3)x^(3/2) de 0 a 1 = 2/3 = 0.666666...
inicio_dificil = 0.0
fim_dificil = 1.0
epsilon_dificil = 1e-6

print(f"\n--- Teste com a função f(x) = sqrt(x) (com singularidade em 0) ---")
print(f"\nCalculando a integral de f(x) = sqrt(x) de {inicio_dificil} a {fim_dificil} com precisão = {epsilon_dificil}")
resultado_dificil = integrar_adaptativo(funcao_dificil, inicio_dificil, fim_dificil, epsilon_dificil)

print(f"Resultado da Integral: {resultado_dificil}")
print(f"Número de avaliações da função f: {funcao_dificil.contador_avaliacoes}")
print(f"Valor real (para sqrt(x) de 0 a 1): {2 / 3}")