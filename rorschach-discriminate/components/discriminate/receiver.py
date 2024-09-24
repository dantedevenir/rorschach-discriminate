from nite_howl import NiteHowl, minute
from os import getenv
import time 

class Receiver:
    def __init__(self):
        broker = getenv('BROKER')
        topic = getenv('TOPIC')
        group = getenv('GROUP')
        self.howler = NiteHowl(broker, group, topic)
    def catch(self):
            radar_generator = self.howler.radar()
            while True:
                try:
                    minute.register("info", f"Searching transform topics...")
                    table, topic = next(radar_generator)
                    self.discriminate(table.to_pandas(), topic)
                except StopIteration:
                    # Si radar_generator se agota, crea una nueva instancia
                    radar_generator = self.howler.radar()
                # Pausa breve para no saturar el bucle
                time.sleep(0.1)
                
                
    def discriminate(self, dataframe, topic):
        policy_from_crm = self.from_query_crm(enumProvider.Name(topic).name, self.broker)
        df_copy = policy_from_crm.df.copy()
        df_copy['expiration_date'] = pd.to_datetime(df_copy['expiration_date'], format='%m-%d-%Y')
        df_sorted = df_copy.sort_values(by=['member_id', 'expiration_date'], ascending=[True, False])
        df_unique = df_sorted.drop_duplicates(subset='member_id', keep='first')
        policy_from_crm.df = df_unique

        dataframe['expiration_date'] = pd.to_datetime(dataframe['expiration_date'], format='%m-%d-%Y')
        left_inner, right_inner, left_outer, right_outer = self.diff(dataframe, policy_from_crm.df)
        full_outer = pd.concat([left_outer, right_outer], axis=0).reset_index(drop=True)
        
        #self.commit(left_inner, right_inner)
        #self.commit(full_outer)
        self.howler.send(f'{topic}_full', df=df_full)

        