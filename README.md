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

---

## 🧱 Architecture

```
CPACS → Reader → Geometry → Modules → Results
```

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

### Python Dependencies

```bash
pip install numpy numba
```

---

## 🧩 External Dependencies (Required)

AeroFrame depends on:

* TiXI 3 (CPACS XML handling)
* TiGL 3 (geometry engine)

These must be installed manually.

---

### 🔽 Step 1 — Download Libraries

Download precompiled binaries from:

* [https://dlr-sc.github.io/tixi/](https://github.com/DLR-SC/tixi)
* [https://dlr-sc.github.io/tigl/](https://github.com/DLR-SC/tigl)

Install or extract them to a directory, e.g.:

```
C:\libs\
  ├── TIXI-3.x.x
  └── TIGL-3.x.x
```

---

### 📁 Step 2 — Set Library Location

You have two options:

---

#### Option A (Recommended): Environment Variable

Set:

```bash
AEROFRAME_LIBS=C:\libs
```

---

#### Option B: Modify Default Path

Edit in:

```
utils/environment.py
```

```python
base = r"C:\path\to\your\libs"
```

---

### ⚙️ Step 3 — Runtime Setup

AeroFrame automatically configures paths via:

```python
from utils.environment import setup_environment
setup_environment()
```

This:

* adds DLL paths
* patches library resolution
* registers Python bindings

---

## ▶️ Usage

Run the full pipeline:

```bash
python run.py
```

---

## 📄 CPACS Integration

AeroFrame uses CPACS as the **single source of truth**.

Custom analysis inputs are defined in:

```xml
/vehicles/aircraft/model/toolspecific/aeroFrame/
```

Example:

```xml
<aerodynamics>
  <parasiteDragCoefficient>0.025</parasiteDragCoefficient>
  <oswaldEfficiency>0.78</oswaldEfficiency>
</aerodynamics>
```

---

## 🧠 Design Philosophy

* Modular and extensible
* No tight coupling between subsystems
* CPACS-driven workflow
* Separation of physics and IO

---

## 📜 License

GPL-3.0 license
