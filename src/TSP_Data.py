class TSP_Data:
    def __init__(self):
        self.data_dict = {

        }

    def add_data(self, generation: int, dist: float):
        data_lst = []
        if generation in self.data_dict:
            data_lst = self.data_dict[generation]
            data_lst.append(dist)
            self.data_dict[generation] = data_lst
        else:
            data_lst.append(dist)
            self.data_dict[generation] = data_lst
