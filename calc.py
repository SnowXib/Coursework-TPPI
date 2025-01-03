import math
from art import text2art
from random import random


class MathCalc:
    """
    Подсчет всех необходмых данных для курсовой

    Args:
        Ft (int): тяговое усилие на приводном барабане транспортера в Кн
        V (float): скорость ленты транспортера
        D (int): диаметр приводного барабана в мм
        P_out (float): Требуемая мощность рабочей машины
        n_out (float): частота вращение приводного вала конвейера
        T_out (float): вращающий момент
        P_ed (float): мощность электродвигателя
        n_ed (float): частота электродвигателя
        n_our (float): КПД
        i_out (float): общее передаточное отношения привода
        P_db (float): требуемая мощность двигателя
        u (float): общее передаточное число
        u_op (float): передаточное число открытой цилиндрической передачи
        error (dict): информация о ошибках
    """
    def __init__(self, scheme_type='Б',Ft=3, V=0.85, D=315, P_out=None, n_out=None, t_out=None, P_ed=None, n_ed=None, n_our=None,
        types_gear=[{'count': 1, 'coef_gear': 0.98, 'open_or_closed': None},
                    {'count': 1, 'coef_gear': 0.97, 'open_or_closed': 'Close'}, 
                    {'count': 1, 'coef_gear': 0.95, 'open_or_closed': 'Open'}, 
                    {'count': 1, 'coef_gear': 0.99, 'open_or_closed': None}],
        i_our=None, P_db=None, u=None, T_dv=None, u_op=None, i_reducer=None, type_gear='Зубчатая цилиндрическая', 
        type_reducer='Зубчатый цилиндрический', P_t=None, P_b=None, P_ed_tr=None):

        U_CP = 5.5 

        self.error = {}
                        
        self.Ft = Ft * 1000
        self.V = V
        self.D = D / 1000 

        self.P_out = (Ft * V) if P_out is None else P_out
        self.n_out = (60 * V * 1000) / (math.pi * D) if n_out is None else n_out
        self.T_out = (0.5 * Ft * D * 10 ** -3) if t_out is None else t_out
        self.P_ed = (self.Ft * self.V) if P_ed is None else P_ed

        P_ed_kilo = self.P_ed / 1000

        if n_ed is None:
            engine_data = [
                (0.37, 0.55, 1357, '71А4'),
                (0.55, 0.75, 1350, '71B4'),
                (0.75, 1.1, 1395, '80A4'),
                (1.1, 1.5, 1395, '80B4'),
                (1.5, 2.2, 1395, '90L4'),
                (2.2, 3, 1410, '100S4'),
                (3, 4, 1410, '100L4'),
                (4, 5.5, 1432, '112M4'),
                (5.5, 7.5, 1440, '132S4'),
                (7.5, 11, 1447, '132M4'),
                (11, 15, 1455, '160S4')
            ]

            for min_val, max_val, n_ed_value, type_engine_value in engine_data:
                if min_val < P_ed_kilo <= max_val:
                    self.n_ed = n_ed_value
                    self.type_engine = type_engine_value
                    break

                else:
                    if P_ed_kilo <= 0.37:
                        self.error['P_ed'] = f'Error P_ed is too low. P_ed: {self.P_ed}'
                        self.type_engine = 'error'
                        self.n_ed = 'error'

        else:
            self.n_ed = n_ed

        if n_our is None:
            n_our = 0
            for gear in types_gear:
                if not n_our:
                    n_our += pow(gear['coef_gear'], gear['count'])
                    continue
                n_our *= pow(gear['coef_gear'], gear['count'])

            self.n_our = n_our
        else:
            self.n_our = n_our

        self.P_ed_tr = self.P_out / self.n_our

        self.i_our = self.n_ed / self.n_out if i_our is None else i_our
        self.P_db = self.P_ed / self.n_our if P_db is None else P_db
        self.u = self.n_ed / self.n_out if u is None else u

        u_op_raw = self.u / U_CP if u_op is None else u_op

        # ГОСТ 2185-66
        u_op_gost = [
            (0.0, 1.0),
            (1.0, 1.12),
            (1.12, 1.25),
            (1.25, 1.4),
            (1.4, 1.6),
            (1.6, 1.8),
            (1.8, 2.0),
            (2.0, 2.24),
            (2.24, 2.5),
            (2.5, 2.8),
            (2.8, 3.15),
            (3.15, 3.55),
            (3.55, 4.0),
            (4.0, 4.5),
            (4.5, 5.0),
            (5.0, 5.6),
            (5.6, 6.3),
            (6.3, 7.1),
            (7.1, 8.0),
            (8.0, 9.0),
            (9.0, 10.0),
            (10.0, 11.2),
            (11.2, 12.5)
        ]

        for min_val, max_val in u_op_gost:
            if min_val < u_op_raw <= max_val:
                self.u_op = max_val
                break
            
            else:
                if u_op_raw < 0:
                    self.error['u_op'] = f'Error u_op_raw is too low. u_op: {u_op_raw}'
                    self.u_op = 'error'
                elif u_op_raw > 12.5:
                    self.error['u_op'] = f'Error u_op_raw is too huge. u_op: {u_op_raw}'
                    self.u_op = 'error'

        u_f = U_CP * self.u_op

        diff_u = abs((u_f - self.u)/(self.u)) * 100 # Отклонение фактического общего передаточного числа

        if diff_u > 6:
            self.error['diff_u'] = f'Error diff_u is too huge. diff_u: {diff_u}'

        i_op_table = {'Зубчатая цилиндрическая': (4.0, 8.0),
                      'Зубчатая коническая': (2.0, 4.0),
                      'Цепная': (1.5, 5.0),
                      'С зубчатым ремнем': (2.0, 8.0),
                      'Клино-ременная': (2.0, 4.0),
                      'Плоско-ременная': (2.0, 2.0)}
        
        i_reducer_table = {'Зубчатый цилиндрический': (1.6, 8.0),
                           'Зубчатый конический': (1.0, 6.3),
                           'Зубчатый планетарный': (3.15, 8.0),
                           'Зубчатый волновой': (70.0, 320.0),
                           'Червячный': (8.0, 63.0)}

        i_op_state = i_op_table[type_gear]
        i_op = i_op_state[1]

        target_i_reducer_state = i_reducer_table[type_reducer]
        correct_bool = False

        while i_op > i_op_state[0]:
            i_reducer = self.i_our / i_op

            if target_i_reducer_state[0] <= i_reducer <= target_i_reducer_state[1]:
                self.i_reducer = i_reducer if i_reducer is None else i_reducer
                correct_bool = True
                break
            else:
                i_op-=0.1
        
        if not correct_bool:
            self.error['i_reducer'] = f'There is no suitable one i_op in range {i_op_state}'

        for gear in types_gear:
            if gear['open_or_closed'] == 'Open':
                nu_op = gear['coef_gear']
            if gear['open_or_closed'] == 'Close':
                nu_zp = gear['coef_gear']

        if scheme_type in ('А', 'Б'):
            self.P_t = self.P_out / (0.99 * nu_op) if P_t is None else P_t

        elif scheme_type in ('В', 'Г'):
            self.P_t = self.P_out / (0.99 * 0.98) if P_t is None else P_t

        self.P_b = self.P_t / nu_zp if P_b is None else P_b 

        if scheme_type in ('А', 'Б'):
            if round(self.P_ed_tr / 1000, 2) != round(self.P_b / 0.98, 2):
                self.error['P_ed'] = f'P_ed does not match the required value. Expected: {round(self.P_ed_tr / 1000, 2)} Received: {round(self.P_b / 0.98, 2)}'
        elif scheme_type in ('В', 'Г'):
            if round(self.P_ed_tr / 1000, 2) != round(self.P_b / nu_op, 2):
                self.error['P_ed'] = f'P_ed does not match the required value. Expected: {round(self.P_ed_tr / 1000, 2)} Received: {round(self.P_b / nu_op, 2)}'


    def __repr__(self):
        return '\n|-'.join([
            ('|-=============================='),
            (f'Ft: {self.Ft} К -- тяговое усилие на приводном барабане транспортера'),
            (f'V: {self.V} м/с -- скорость ленты транспортера'),
            (f'D: {self.D} м -- диаметр приводного барабана'),
            (f'P_out: {self.P_out} кВт -- Требуемая мощность рабочей машины'),
            (f'n_out: {self.n_out} мин**-1 -- частота вращение приводного вала конвейера'),
            (f'T_out: {self.T_out} Кн*мм -- вращающий момент'),
            (f'P_ed: {self.P_ed} кВт -- мощность электродвигателя'),
            (f'n_ed: {self.n_ed} мин**-1 -- частота электродвигателя'),
            (f'type_engine: {self.type_engine} -- тип двигателя'),
            (f'n_our: {self.n_our} -- КПД'),
            (f'i_our: {self.i_our} общее передаточное отношения привода'),
            (f'P_db: {self.P_db} кВт -- требуемая мощность двигателя'),
            (f'u: {self.u} общее передаточное число'),
            (f'u_op: {self.u_op} передаточное число открытой цилиндрической передачи'),
            (f'i_reducer: {self.i_reducer} общее придаточное отношение редуктора'),
            (f'P_t: {self.P_t} мощность тихоходного вала'),
            (f'P_b: {self.P_b} мощность быстроходного вала'),
            (f'error: {self.error} описание ошибки'),
            ('==============================='),
        ])
    
    
    def __iter__(self):
        """
        Возвращает итератор по ключам и значениям атрибутов объекта.

        Returns:
            iter: Итератор, который проходит по элементам словаря атрибутов объекта.
        """
        return iter(self.__dict__.items())


print('Demo режим, для его изменения явно укажите параметры класса')
calc = MathCalc()

label  = text2art("AutoTPPI", font='slant')
print(label)
print(calc)