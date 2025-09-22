# Tutoriel Minimal : Installer VS Code + Python sur votre machine

Ce guide explique comment installer **VS Code**, **Python**, et les bibliothèques classiques (**NumPy**, **Matplotlib**, **IPython**) sur **Windows, macOS et Linux**.

---

## 1. Installer VS Code
- Télécharger depuis [https://code.visualstudio.com](https://code.visualstudio.com)  
- Installer normalement :
  - **Windows** : lancer le `.exe`
  - **macOS** : glisser dans Applications
  - **Linux** : installer le `.deb` ou `.rpm`
- Lancer **Visual Studio Code**.

---

## 2. Installer Python
- Télécharger la dernière version de **Python 3** depuis [https://www.python.org/downloads/](https://www.python.org/downloads/).
- **Windows** : cocher **“Add Python to PATH”** pendant l’installation.
- **macOS / Linux** : Python est souvent déjà présent. Vérifier dans un terminal :
  ```bash
  python3 --version
  ```
  ou sous Windows :
  ```bash
  python --version
  ```

---

## 3. Installer les bibliothèques nécessaires
Ouvrir un terminal (ou PowerShell sous Windows) et taper :
```bash
pip install numpy matplotlib ipython
```

---

## 4. Configurer VS Code
1. Ouvrir **VS Code**  
2. Aller dans l’onglet **Extensions** (`Ctrl+Shift+X`)  
3. Chercher **Python** (éditeur Microsoft) et cliquer sur **Installer**  
4. Ouvrir un fichier `test.py`  
5. Vérifier que VS Code détecte l’installation de Python (choisir l’interpréteur si besoin)

---

## 5. Premier test
Créer un fichier `test.py` :
```python
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 2*np.pi, 100)
plt.plot(x, np.sin(x))
plt.show()
```

Lancer avec :
```bash
python test.py
```

➡️ Si une courbe sinusoïdale apparaît, tout est prêt ✅

---
