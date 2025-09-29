# HW_1–HW_4

Требования: Python ≥ 3.10.  

## Как запускать
```bash
python -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\Activate.ps1
pip install -e .
````

---

## HW01

Папка: `hw_1`
Артефакты:

* `artifacts/1.1/session.txt` — задание 1.1 (nl)
* `artifacts/1.2/session.txt` — задание 1.2 (tail)
* `artifacts/1.3/session.txt` — задание 1.3 (wc)

Запуск:

```bash
python hw_1/scripts/gen_task11.py
python hw_1/scripts/gen_task12.py
python hw_1/scripts/gen_task13.py
```

---

## HW_2 — LaTeX

Папка: `hw_2`
Артефакты:

* `artifacts/hw02_table.tex` (2.1)
* `artifacts/hw02_full.tex`, `hw02_full.pdf` (2.2)
* `Dockerfile` (2.3)

Запуск:

```bash
python scripts/gen_table_tex.py
python scripts/gen_artifacts.py --compile   # требует pdflatex
```

---

## HW_3 — Матрицы

Папка: `hw_3`
Артефакты:

* `artifacts/3.1/`: `matrix+.txt`, `matrix*.txt`, `matrix@.txt`
* `artifacts/3.2/`: `matrix+.txt`, `matrix*.txt`, `matrix@.txt`
* `artifacts/3.3/`: `A.txt`, `B.txt`, `C.txt`, `D.txt`, `AB.txt`, `CD.txt`, `hash.txt`

Запуск:

```bash
python scripts/gen_task31.py
python scripts/gen_task32.py
python scripts/gen_task33.py
```

---

## HW_4 — Параллелизм

Папка: `hw_4`
Артефакты:

* `artifacts/4.1/timings.txt`
* `artifacts/4.2/integrate_timings.csv`
* `artifacts/4.3/session.txt`

Запуск:

```bash
python scripts/task_41_fib_benchmark.py --n 36 --reps 10
python scripts/task_42_integrate.py
python scripts/task_43_pipeline.py    # ввод; завершение Ctrl-D/EOF
```