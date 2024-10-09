import math


class MathCalc:
    """
    Подсчет всех необходмых данных для курсовой

    Args:
        Ft (int): тяговое усилие на приводном барабане транспортера в Кн
        V (float): скорость ленты транспортера
        D (int): диаметр приводного барабана в мм
        P_out (float): энергетическая характеристика
        n_out (float): частота вращение приводного вала конвейера
        T_out (float): вращающий момент
        P_ed (float): мощность электродвигателя
        n_ed (float): частота электродвигателя
        n_our (float): КПД
        i_out (float): общее передаточное отношения привода
        P_db (float): требуемая мощность двигателя
        u (float): общее придаточное число
    """
    def __init__(self, Ft=3, V=0.85, D=315, P_out=None, n_out=None, t_out=None, P_ed=None, n_ed=None, n_our=None,
        types_gear=[{'count': 3, 'coef_gear': 0.99}, {'count': 1, 'coef_gear': 0.98},
                    {'count': 1, 'coef_gear': 0.97}],
        i_our=None, P_db=None, u=None):
                        
        self.Ft = Ft * 1000
        self.V = V
        self.D = 1000 / D 

        self.P_out = (Ft * V) if P_out is None else P_out
        self.n_out = (60 * V * 1000) / (math.pi * D) if n_out is None else n_out
        self.T_out = (0.5 * Ft * D * 10 ** -3) if t_out is None else t_out
        self.P_ed = (self.Ft * self.V) if P_ed is None else P_ed

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
                if min_val < self.P_ed <= max_val:
                    self.n_ed = n_ed_value
                    self.type_engine = type_engine_value
                    break

                else:
                    if self.P_ed <= 0.37:
                        print(f'Error P_ed too low. P_ed: {self.P_ed}')
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

        self.i_our = self.n_ed / self.n_out if i_our is None else i_our
        self.P_db = self.P_ed / self.n_out if P_db is None else P_db
        self.u = self.n_ed / self.n_out if u is None else u

    def __repr__(self):
        return '\n|-'.join([
            ('|-=============================='),
            (f'Ft: {self.Ft} Кн -- тяговое усилие на приводном барабане транспортера'),
            (f'V: {self.V} м/с -- скорость ленты транспортера'),
            (f'D: {self.D} мм -- диаметр приводного барабана'),
            (f'P_out: {self.P_out} кВт -- энергетическая характеристика'),
            (f'n_out: {self.n_out} мин**-1 -- частота вращение приводного вала конвейера'),
            (f'T_out: {self.T_out} Кн*мм -- вращающий момент'),
            (f'P_ed: {self.P_ed} кВт -- мощность электродвигателя'),
            (f'n_ed: {self.n_ed} мин**-1 -- частота электродвигателя'),
            (f'type_engine: {self.type_engine} -- тип двигателя'),
            (f'n_our: {self.n_our} -- КПД'),
            (f'i_our: {self.i_our} общее передаточное отношения привода'),
            (f'P_db: {self.P_db} кВт -- требуемая мощность двигателя'),
            (f'u: {self.u} общее придаточное число'),
            ('==============================='),
        ])


print('Demo режим, для его изменения явно укажите параметры класса')
calc = MathCalc()

print(calc)
