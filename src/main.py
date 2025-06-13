import streamlit as st
from scheduler.genetic_algo import genetic_algorithm
from scheduler.initialization import random_initialization, greedy_initialization
from scheduler.compare import compare_random_vs_optimized
from scheduler.crossover import order_crossover, cyclic_crossover, partially_mapped_crossover
from scheduler.mutation import swap_mutation, scramble_mutation, inversion_mutation
from scheduler.selection import tournament_selection, rank_selection, over_selection
from scheduler.survivor import elitism, genitor, mu_lambda
from scheduler.diversity import extinction_restart, crowding

def main():
    st.title("🏆 Sports Tournament Scheduling with Genetic Algorithm")

    st.header("⚙️ Configuration")


    population_size = st.slider("Population Size", min_value=5, max_value=1000, value=30, step=5)
    generations = st.slider("Number of Generations", min_value=10, max_value=1000, value=200, step=10)
    mutation_rate = st.slider("Mutation Rate", min_value=0.01, max_value=1.0, value=0.2, step=0.01)
    crossover_rate = st.slider("Crossover Rate", min_value=0.1, max_value=1.0, value=0.9, step=0.01)
    stagnation_limit = st.slider("Stagnation Limit", min_value=5, max_value=100, value=25, step=5)
    seed = st.number_input("🌱 Random Seed (for reproducibility)", min_value=0, value=42, step=1)


    crossover_choice = st.selectbox(
        "🔀 Crossover Method",
        options=["Order Crossover", "Cyclic Crossover", "Partially Mapped Crossover(PMX)"],
        index=0
    )

    mutation_choice = st.selectbox(
        "🧬 Mutation Method",
        options=["Scramble Mutation", "Swap Mutation", "Inversion Mutation"],
        index=0
    )

    selection_choice = st.selectbox(
        "👨‍👩‍👧 Parent Selection Method",
        options=["Tournament", "Rank", "Over-Selection"],
        index=0
    )

    if selection_choice == "Tournament":
        tournament_size = st.slider("Tournament Size", min_value=2, max_value=10, value=2, step=1)
        rank_size = None
    elif selection_choice == "Rank":
        tournament_size = None
        rank_size = st.slider("Rank Size", min_value=2, max_value=10, value=2, step=1)
    else:
        rank_size = None
        tournament_size = None

    survivor_choice = st.selectbox(
        "🧹 Survivor Selection Method",
        options=["Elitism", "Genitor", "(μ,λ)-Selection"],
        index=0
    )

    if survivor_choice == "Elitism":
        top_n_elitism = st.slider("Top N Elitism", min_value=1, max_value=10, value=5, step=1)
        replace_count = None
    elif survivor_choice == "Genitor":
        top_n_elitism = None
        replace_count = st.slider("Replace Count", min_value=1, max_value=10, value=3, step=1)
    else:
        top_n_elitism = st.slider("μ (Selection Size)", min_value=1, max_value=10, value=5, step=1)
        replace_count = None

    diversity_choice = st.selectbox(
        "🌐 Diversity Mechanisms",
        options=["Crowding", "Extinction", "Both"],
        index=0
    )

    if diversity_choice == "Extinction":
        extinction_keep_ratio = st.slider("Extinction Keep Ratio", min_value=0.1, max_value=0.9, value=0.66, step=0.01)
        crowding_factor = None
    elif diversity_choice == "Crowding":
        crowding_factor = st.slider("Crowding Factor", min_value=0.01, max_value=1.0, value=0.2, step=0.01)
        extinction_keep_ratio = None
    elif diversity_choice == "Both":
        col1, col2 = st.columns(2)
        with col1:
            extinction_keep_ratio = st.slider("Extinction Keep Ratio", min_value=0.1, max_value=0.9, value=0.66, step=0.01)
        with col2:
            crowding_factor = st.slider("Crowding Factor", min_value=0.01, max_value=0.9, value=0.66, step=0.01)

    crossover_methods = {
        "Order Crossover": order_crossover,
        "Cyclic Crossover": cyclic_crossover,
        "Partially Mapped Crossover(PMX)": partially_mapped_crossover
    }
    crossover_method = crossover_methods[crossover_choice]

    mutation_methods = {
        "Scramble Mutation": scramble_mutation,
        "Swap Mutation": swap_mutation,
        "Inversion Mutation": inversion_mutation
    }
    mutation_method = mutation_methods[mutation_choice]

    selection_methods = {
        "Tournament": tournament_selection,
        "Rank": rank_selection,
        "Over-Selection": over_selection
    }
    selection_method = selection_methods[selection_choice]

    survivor_methods = {
        "Elitism": elitism,
        "Genitor": genitor,
        "(μ,λ)-Selection": mu_lambda
    }
    survivor_method = survivor_methods[survivor_choice]

    diversity_methods = {
        "Crowding": crowding,
        "Extinction": extinction_restart,
        "Both": crowding and extinction_restart
    }
    diversity_method = diversity_methods[diversity_choice]

    if st.button("Generate Optimized Schedule"):
        initial_random_population = random_initialization(population_size , seed = seed)

        optimized_random_population, penalties_per_gen_r = genetic_algorithm(
            population_size=population_size,
            generations=generations,
            crossover_method=crossover_method,
            mutation_method=mutation_method,
            initial_mutation_rate=mutation_rate,
            crossover_probability=crossover_rate,
            rank_size=rank_size if selection_choice == "Rank" else None,
            tournament_size=tournament_size if selection_choice == "Tournament" else None,
            top_n_elitism=top_n_elitism,
            replace_count=replace_count if survivor_choice == "Genitor" else None,
            selection_method=selection_method,
            survivor_method=survivor_method,
            initial_population=initial_random_population,
            stagnation_limit=stagnation_limit,
            diversity_method=diversity_method,
            crowding_factor=crowding_factor,
            extinction_keep_ratio=extinction_keep_ratio,
            seed=seed
        )

        optimized_random_schedule = optimized_random_population[0]

        initial_greedy_population = greedy_initialization(population_size , seed =seed)

        optimized_greedy_population, penalties_per_gen_g = genetic_algorithm(
            population_size=population_size,
            generations=generations,
            crossover_method=crossover_method,
            mutation_method=mutation_method,
            initial_mutation_rate=mutation_rate,
            crossover_probability=crossover_rate,
            rank_size=rank_size if selection_choice == "Rank" else None,
            tournament_size=tournament_size if selection_choice == "Tournament" else None,
            top_n_elitism=top_n_elitism,
            replace_count=replace_count if survivor_choice == "Genitor" else None,
            selection_method=selection_method,
            survivor_method=survivor_method,
            initial_population=initial_greedy_population,
            stagnation_limit=stagnation_limit,
            diversity_method=diversity_method,
            crowding_factor=crowding_factor,
            extinction_keep_ratio=extinction_keep_ratio,
            seed=seed
        )

        optimized_greedy_schedule = optimized_greedy_population[0]

        random_schedule = random_initialization(1)[0]
        greedy_schedule = greedy_initialization(1)[0]

        comparison_r = compare_random_vs_optimized(random_schedule, optimized_random_schedule)
        comparison_g = compare_random_vs_optimized(greedy_schedule, optimized_greedy_schedule)

        
        # st.subheader("🗓️ Random Schedule")
        # st.dataframe(comparison_r["Random Schedule Data"])

        st.subheader("🏆 Optimized Random Schedule")
        st.dataframe(comparison_r["Optimized Schedule Data"])

        

        # st.subheader("🗓️ Greedy Schedule")
        # st.dataframe(comparison_g["Random Schedule Data"])

        st.subheader("🏆 Optimized Greedy Schedule")
        st.dataframe(comparison_g["Optimized Schedule Data"])

        st.header("🔍 Results")

        st.write(f"🔹 Random Schedule Penalty: **{comparison_r['Random Schedule Penalty']}**")
        st.write(f"✅ Optimized Schedule Penalty: **{comparison_r['Optimized Schedule Penalty']}**")
        st.write(f"📉 Improvement: **{comparison_r['Improvement in Penalty']}**")

        st.write(f"🔹 Greedy Schedule Penalty: **{comparison_g['Random Schedule Penalty']}**")
        st.write(f"✅ Optimized Greedy Schedule Penalty: **{comparison_g['Optimized Schedule Penalty']}**")
        st.write(f"📉 Improvement: **{comparison_g['Improvement in Penalty']}**")


        st.subheader("📈 Penalty Progress Over Generations")
        st.line_chart({
            "Random Initialization": penalties_per_gen_r,
            "Greedy Initialization": penalties_per_gen_g
        })

if __name__ == "__main__":
    main()