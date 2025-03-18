import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
from skfuzzy import control as ctrl

# Definição das variáveis fuzzy
consumo = ctrl.Antecedent(np.arange(0, 11, 1), 'consumo') # 0 a 10 mil kcal
peso = ctrl.Antecedent(np.arange(0, 11, 1), 'peso') # 0 a 10 kg
obesidade = ctrl.Consequent(np.arange(0, 11, 1), 'obesidade')

# Definição das funções de pertinência
consumo['pouco'] = fuzz.trimf(consumo.universe, [0, 2, 4])
consumo['razoavel'] = fuzz.trimf(consumo.universe, [3, 5, 7])
consumo['bastante'] = fuzz.trimf(consumo.universe, [6, 8, 10])

peso['leve'] = fuzz.trimf(peso.universe, [0, 2, 4])
peso['medio'] = fuzz.trimf(peso.universe, [3, 5, 7])
peso['pesado'] = fuzz.trimf(peso.universe, [6, 8, 10])

obesidade['baixa'] = fuzz.trimf(obesidade.universe, [0, 2, 4])
obesidade['moderada'] = fuzz.trimf(obesidade.universe, [3, 5, 7])
obesidade['alta'] = fuzz.trimf(obesidade.universe, [6, 8, 10])

# Definição das regras fuzzy
regra1 = ctrl.Rule(consumo['pouco'] & peso['leve'], obesidade['baixa'])
regra2 = ctrl.Rule(consumo['razoavel'] & peso['medio'], obesidade['moderada'])
regra3 = ctrl.Rule(consumo['bastante'] & peso['pesado'], obesidade['alta'])
regra4 = ctrl.Rule(consumo['pouco'] & peso['pesado'], obesidade['moderada'])
regra5 = ctrl.Rule(consumo['bastante'] & peso['leve'], obesidade['moderada'])

# Criar o sistema de controle
sistema_controle = ctrl.ControlSystem([regra1, regra2, regra3, regra4, regra5])
simulacao = ctrl.ControlSystemSimulation(sistema_controle)

# Entrada do usuário
consumo_usuario = float(input("Digite o nível de consumo (0 a 10): "))
peso_usuario = float(input("Digite o peso (0 a 10): "))

simulacao.input['consumo'] = consumo_usuario
simulacao.input['peso'] = peso_usuario
simulacao.compute()

# Saída
print(f"Grau de Obesidade: {simulacao.output['obesidade']:.2f}")

# Visualizar as funções de pertinência
consumo.view()
peso.view()
obesidade.view(sim=simulacao)
plt.show()