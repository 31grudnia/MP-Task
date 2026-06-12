
# Solar Array Calculator 🫪

A stateless, interface-driven Python utility designed to calculate the precise coordinates of structural supports (**mounts**) and inter-panel **joints** for solar arrays. 

---

## 🚀 Getting Started

The easiest way to build, test, and run the entire pipeline is to use the automated shell script.

### 📋 Prerequisites
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

### ⚡ Run Everything (One Command)
Make the runner script executable and run it. This will build the container, execute the entire test suite, and print the serialized JSON output of the pipeline:
```bash
chmod +x run.sh
./run.sh
```

## 🧪 Edge Cases Covered
The test suite in `tests/` comprehensively verifies:
* **The "Impossible Roof" layout** (handling contradictory geometric constraints).
* **Asymmetric Grid Intersections** (preventing false joint merges over solid panels).
* **"Single Panel, Multiple Mounts"** (verifying safety limits on isolated panels).
* **"Broken Tooth" layout** (segmenting non-continuous rows correctly).

# 🫪 🫪 🫪
