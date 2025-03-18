import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
from skfuzzy import control as ctrl

# Variáveis de entrada
consumo = ctrl.Antecedent(np.arange(0, 11, 1), 'consumo')
peso = ctrl.Antecedent(np.arange(0, 11, 1), 'peso')
atividade_fisica = ctrl.Antecedent(np.arange(0, 11, 1), 'atividade_fisica')

# Variável de saída
obesidade = ctrl.Consequent(np.arange(0, 11, 1), 'obesidade')

# Funções de pertinência
consumo['pouco'] = fuzz.trapmf(consumo.universe, [0, 0, 2, 4])
consumo['razoavel'] = fuzz.trimf(consumo.universe, [3, 5, 7])
consumo['bastante'] = fuzz.trapmf(consumo.universe, [6, 8, 10, 10])

peso['leve'] = fuzz.trapmf(peso.universe, [0, 0, 2, 4])
peso['medio'] = fuzz.trimf(peso.universe, [3, 5, 7])
peso['pesado'] = fuzz.trapmf(peso.universe, [6, 8, 10, 10])

atividade_fisica['baixa'] = fuzz.trapmf(atividade_fisica.universe, [0, 0, 2, 4])
atividade_fisica['moderada'] = fuzz.trimf(atividade_fisica.universe, [3, 5, 7])
atividade_fisica['alta'] = fuzz.trapmf(atividade_fisica.universe, [6, 8, 10, 10])

obesidade['baixa'] = fuzz.trapmf(obesidade.universe, [0, 0, 2, 4])
obesidade['moderada'] = fuzz.trimf(obesidade.universe, [3, 5, 7])
obesidade['alta'] = fuzz.trapmf(obesidade.universe, [6, 8, 10, 10])

# Regras
regras = [
    ctrl.Rule(consumo['pouco'] & peso['leve'] & atividade_fisica['alta'], obesidade['baixa']),
    ctrl.Rule(consumo['razoavel'] & peso['medio'] & atividade_fisica['moderada'], obesidade['moderada']),
    ctrl.Rule(consumo['bastante'] & peso['pesado'] & atividade_fisica['baixa'], obesidade['alta']),
    ctrl.Rule(consumo['bastante'] & peso['medio'] & atividade_fisica['alta'], obesidade['moderada']),
    ctrl.Rule(consumo['pouco'] & peso['pesado'] & atividade_fisica['baixa'], obesidade['alta']),
    ctrl.Rule(consumo['razoavel'] & peso['leve'] & atividade_fisica['moderada'], obesidade['baixa']),
    ctrl.Rule(consumo['razoavel'] & peso['pesado'] & atividade_fisica['alta'], obesidade['moderada']),
    ctrl.Rule(consumo['pouco'] & peso['medio'] & atividade_fisica['alta'], obesidade['baixa']),
    ctrl.Rule(consumo['bastante'] & peso['leve'] & atividade_fisica['alta'], obesidade['moderada'])
]

# Criando o sistema
sistema_controle = ctrl.ControlSystem(regras)
simulacao = ctrl.ControlSystemSimulation(sistema_controle)

# Entrada do usuário
consumo_usuario = float(input("Consumo (0 a 10): "))
peso_usuario = float(input("Peso (0 a 10): "))
atividade_usuario = float(input("Atividade física (0 a 10): "))

simulacao.input['consumo'] = consumo_usuario
simulacao.input['peso'] = peso_usuario
simulacao.input['atividade_fisica'] = atividade_usuario
simulacao.compute()

# Resultado
print(f"Grau de Obesidade: {simulacao.output['obesidade']:.2f}")

# Visualização
consumo.view()
peso.view()
atividade_fisica.view()
obesidade.view(sim=simulacao)
plt.show()
