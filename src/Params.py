class Param:
    def __init__(self):
        self.population_size_nsg: int = 10
        self.evaluations_tsp: int = 10
        self.run_local_tsp: bool = True
        self.tournament_size_ksp: int = 2
        self.num_generations_ksp: int = 100
        self.fill_rate_ksp: float = 0.5

