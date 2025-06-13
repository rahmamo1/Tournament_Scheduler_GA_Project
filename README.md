# 🏆 Tournament Scheduler with Genetic Algorithms
This project builds a smart scheduler for sports tournaments using Genetic Algorithms (GAs). It creates fair and efficient match schedules by avoiding issues like stadium conflicts and unfair rest periods.

## 🎯 Goals of the Project
•	Automatically generate tournament schedules (e.g., round-robin).

•	Avoid common scheduling issues such as:

      o	Conflicting use of stadiums
      
      o	Uneven rest time between matches
      
      o	Imbalanced match distribution

•	Improve results using evolutionary techniques like GA and coevolution.

•	Compare multiple methods and visualize the outcomes.

•	Offer a simple user interface to interact with the scheduler.


## 🛠️ Tools and Libraries
| Task                       | Libraries Used                    |
| -------------------------- | --------------------------------- |
| Genetic Algorithm Engine   | `DEAP`, `PyGAD`                   |
| Constraints & Optimization | `NumPy`, `PuLP`                   |
| Visualization              | `Matplotlib`, `Plotly`, `Pandas`  |
| User Interface (Optional)  | `Streamlit`, `Tkinter`            |
| Logging & Experimentation  | `SciPy`, `logging`, `PrettyTable` |

## ⚙️ How It Works
•	Schedules are represented as individuals in a GA population.

•	Fitness function checks for:

      o	Double-booked venues
      
      o	Fair rest periods
      
      o	Balanced scheduling

•	GA operators include:

      o	Selection: Tournament, Roulette
      
      o	Crossover: Order crossover (OX), PMX
      
      o	Mutation: Swap, Insertion

•	Optionally, a multi-island approach can be used to evolve solutions in parallel.


## 🔍 What We Test
The project compares different configurations by changing:
•	Population size

•	Mutation and crossover types

•	Constraint handling methods
Results are visualized using graphs to show how the fitness improves over generations. Baseline methods like greedy algorithms are also compared.

## 📊 Outputs
•	Final match schedules are saved in results/schedules/

•	Performance graphs and logs are saved in results/plots/ and results/logs/

## ✅ Final Deliverables
•	A working Python tool that creates valid tournament schedules

•	Built-in constraint handling for real-world scenarios

•	Charts, comparisons, and a GUI for exploration

•	A full write-up documenting the approach and findings
