from Dataset_creation.Simulator import Simulator

if __name__ == '__main__':
    simulator = Simulator()
    df = simulator.get_simulated_df(num_rows=20000)

    df = df.sample(500)
    df.to_csv('data/df_simulated.csv', index=False)
