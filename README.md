# AeroFrame ✈️

AeroFrame is a modular aircraft analysis framework built in Python using **CPACS**, **TiXI**, and **TiGL**.
It follows a **Model-Based Systems Engineering (MBSE)** approach to enable clean, extensible aircraft design workflows.

---

## 🚀 Features

* CPACS-driven aircraft definition
* Geometry extraction using TiGL
* Modular analysis:

  * Aerodynamics (lifting-line model)
  * Weight estimation
  * Performance (Breguet range)
* Clean architecture with strong separation of concerns
* Extensible for research and engineering workflows

---

## 🧱 Architecture

```
CPACS → Reader → Geometry → Modules → Results
```

### Modules:

* **Geometry**: Wing properties via TiGL
* **Aerodynamics**: Lift, drag, L/D
* **Weight**: Parametric or CPACS-driven
* **Performance**: Range estimation

---

## 📂 Project Structure

```
AeroFrame/
│
├── core/           # Data models & pipeline
├── interfaces/     # CPACS (TiXI) interface
├── geometry/       # TiGL geometry extraction
├── modules/        # Aero, weight, performance
├── utils/          # Numerics & environment setup
├── data/           # CPACS files
├── tests/          # Unit tests
└── run.py          # Entry point
```

---

## ⚙️ Requirements

* Python 3.10+
* NumPy
* Numba
* TiXI 3
* TiGL 3

---

## ▶️ Usage

1. Configure environment:

```python
from utils.environment import setup_environment
setup_environment()
```

2. Run analysis:

```bash
python run.py
```

---

## 📄 CPACS Integration

AeroFrame uses CPACS as the **single source of truth**.

Custom analysis inputs are stored under:

```xml
/toolspecific/aeroFrame/
```

---

## 🧠 Design Philosophy

* Modular and extensible
* No tight coupling between subsystems
* CPACS-driven data flow
* Clean separation of physics and IO

---

## 📜 License

GNU GENERAL PUBLIC LICENSE
