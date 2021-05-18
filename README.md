# Elliptic Curve Factorization
[![](https://img.shields.io/pypi/v/pyecf.svg?style=flat-square)](https://pypi.org/project/pyecf/)

Данный модуль предназначен для нахождения всех делителей числа 
(факторизация, разложение на простые множители). В качестве метода факторизации
используется [алгоритм](https://wstein.org/edu/124/lenstra/lenstra.pdf), предложенный Хендриком Ленстрой в 1987 году.

## Зависимости
Для проверки простоты числа используется библиотека *sage*. Перед использованием, в выбранном окружении 
(*venv*, *conda*) необходимо установить библиотеку:
```shell
# for pip usage (venv)
pip install sagemath

# for conda usage create new environment
conda config --add channels conda-forge
conda config --set channel_priority strict
conda create -n sage sage python=3.8
```

## Использование через командную строку
Для использования в терминале достаточно установить пакет:
```shell
git clone https://github.com/NikitaYurasov/ECF.git
cd ECF
```
И выполнить следующую команду:
```shell
python pyecf -n 9671406556917033397649407
```

## Использование в Python
Пакет выложен на PyPi, так что достаточно просто установить его через *pip*:
```shell
pip install pyecf
```
Внутри проекта использование может выглядеть так:
```python
from pyecf import LenstraAlgorithm

n = 9671406556917033397649407
algo = LenstraAlgorithm(n)
factors = algo.factorize() # factors - отсортированный список делителей
```